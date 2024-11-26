import logging

from bson.errors import InvalidId
from fastapi import APIRouter, File, UploadFile, status, HTTPException, Depends
from fastapi.responses import JSONResponse, Response
from bson.objectid import ObjectId

from decryptor.file_service import FileService
from app.decryptor.decryptor_service import DecryptorService
from app.running_config.running_config_service import RunningConfigService
from app.repository.topology_repository import TopologyRepository
from app.repository.decrypted_xml_repository import DecryptedXMLRepository
from app.config_upload.config_upload_service import ConfigUploadService
from app.config_upload.exceptions.config_upload_exceptions import (
    DeviceBuildError,
    DeviceConfigError,
    DeviceConnectionError
)
from app.running_config.util.device_config_types import DeviceConfigInfo

router = APIRouter(prefix="/config_upload")


@router.post("/upload_pkt")
async def upload_pkt(
        file: UploadFile = File(...),
        file_service: FileService = Depends(FileService),
        force_overwrite: bool = False
) -> Response:
    """
    Uploads a PKT file to server. The file must have a .pkt extension.
    :param file: File object
    :param force_overwrite: Whether to overwrite an existing file with the same name
    :return: Response
    """
    if not file.filename.endswith(".pkt"):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid file type")

    try:
        content = file.file.read()
        file_service.save_file(content, file.filename, force_overwrite=force_overwrite)
    except FileExistsError as fee:
        logging.error(fee)
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED)
    except Exception as ex:
        logging.error(ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await file.close()
        logging.info(f"Successfully uploaded and saved {file.filename}")
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/decrypt_pkt")
def decrypt_pkt(
        name: str,
        file_service: FileService = Depends(FileService),
        decryptor_service: DecryptorService = Depends(DecryptorService),
) -> JSONResponse:
    """
    Decrypts a PKT file to XML and saves the content to database
    :param name: Name of the target PKT file (must be previously uploaded!).
    :return: JSONResponse
    """

    if not file_service.check_file_exists(name):
        logging.error(f"File {name} does not exist.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"File {name} does not exist.")

    xml_path = decryptor_service.decrypt_pkt(name)

    xml_id = decryptor_service.save_xml_to_database(xml_path)
    response = {
        "xml_id": xml_id
    }

    logging.info("Successfully decrypted XML and uploaded it do database.")
    return JSONResponse(status_code=status.HTTP_200_OK, content=response)


@router.post("/extract_xml/{xml_id}")
async def extract_config(
        xml_id: str,
        running_config_service: RunningConfigService = Depends(RunningConfigService),
        topology_repository: TopologyRepository = Depends(TopologyRepository),
        decrypted_xml_repository: DecryptedXMLRepository = Depends(DecryptedXMLRepository)
) -> JSONResponse:
    try:
        topology_id = ObjectId(xml_id)
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="topology_id has invalid format")

    topology_dict = decrypted_xml_repository.find_one({"_id": ObjectId(topology_id)})
    topology_config = running_config_service.get_configs_for_upload(topology_dict)

    if not topology_config.topology:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Topology was either empty or invalid.")

    topology_id = topology_repository.insert(topology_config)
    response = {
        "topology_id": topology_id
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=response)


@router.post("/topologies/{topology_id}/configure-devices")
async def configure_devices(
        topology_id: str,
        topology_repository: TopologyRepository = Depends(TopologyRepository),
        config_upload_service: ConfigUploadService = Depends(ConfigUploadService)
) -> JSONResponse:
    try:
        topology_id = ObjectId(topology_id)
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="topology_id has invalid format")

    topology: list[DeviceConfigInfo] = topology_repository.find_by_id(topology_id)
    if not topology:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topology not found")

    try:
        devices = config_upload_service.build_netmiko_devices(topology)
    except DeviceBuildError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to build device")

    try:
        config_upload_service.upload_configs(devices)
    except DeviceConnectionError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Connection error while configuring devices. Error: {e}")
    except DeviceConfigError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to send config to device. Error: {e}")

    return JSONResponse(content="Config uploaded successfully", status_code=status.HTTP_200_OK)
