import logging

from bson.errors import InvalidId
from fastapi import APIRouter, File, UploadFile, status, HTTPException, Depends, Query
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from bson.objectid import ObjectId

from app.decryptor.file_service import FileService
from app.decryptor.decryptor_service import DecryptorService
from app.mapping.mapping_service import MappingService
from app.models.mapping import MappingModel
from app.repository.mapping_repository import MappingRepository
from app.running_config.running_config_service import RunningConfigService
from app.repository.topology_repository import TopologyRepository
from app.repository.decrypted_xml_repository import DecryptedXMLRepository
from app.config_upload.config_upload_service import ConfigUploadService
from app.config_upload.exceptions.config_upload_exceptions import (
    DeviceBuildError,
    DeviceConfigError,
    DeviceConnectionError
)

router = APIRouter(prefix="/config_upload")


@router.get("/list_xml_names")
def list_xml_names(xml_repo: DecryptedXMLRepository = Depends(DecryptedXMLRepository)):
    names = xml_repo.list_names()
    return JSONResponse(content=names)

@router.post("/upload_pkt")
async def upload_pkt(
        file: UploadFile = File(...),
        force_overwrite: bool = False,
        file_service: FileService = Depends(FileService),
        decryptor_service: DecryptorService = Depends(DecryptorService),
        xml_repo: DecryptedXMLRepository = Depends(DecryptedXMLRepository)
) -> JSONResponse:
    """
    Decrypts a PKT file to XML and saves the content to database
    :return: JSONResponse
    """

    # Upload
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


    # Decrypt
    if not file_service.check_file_exists(file.filename):
        logging.error(f"File {file.filename} does not exist.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"File {file.filename} does not exist.")

    xml_path = decryptor_service.decrypt_pkt(file.filename)

    # TODO fix force_overwrite
    xml_id = decryptor_service.save_xml_to_database(xml_path)
    response = xml_repo.list_names()

    logging.info("Successfully decrypted XML and uploaded it do database.")
    return JSONResponse(status_code=status.HTTP_200_OK, content=response)


@router.get("/extract_xml/{xml_id}")
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

    xml_model = decrypted_xml_repository.find_object({"_id": ObjectId(topology_id)})
    topology_config = running_config_service.get_configs_for_upload(xml_model)

    if not topology_config.topology:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Topology was either empty or invalid.")

    topology_id = topology_repository.insert(topology_config)
    response = {
        "topology_id": str(topology_id)
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=response)


@router.post("/configure-devices/{lab_group_number}")
async def configure_devices(
        lab_group_number: int,
        mapping_repository: MappingRepository = Depends(MappingRepository),
        config_upload_service: ConfigUploadService = Depends(ConfigUploadService)
) -> JSONResponse:
    mapped_devices = mapping_repository.find_devices_by_group(lab_group_number)
    if not mapped_devices:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Devices not found for group {lab_group_number}.")

    try:
        netmiko_devices = config_upload_service.build_netmiko_devices(mapped_devices)
    except DeviceBuildError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to build netmiko device")

    try:
        config_upload_service.upload_configs(netmiko_devices)
    except DeviceConnectionError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Connection error while configuring devices. Error: {e}")
    except DeviceConfigError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to send config to device. Error: {e}")

    return JSONResponse(content="Config uploaded successfully", status_code=status.HTTP_200_OK)


@router.get("/topologies/{topology_id}/mapping")
def get_device_mapping(topology_id: str,
                       group_id: list[int] | None = Query(default=None),
                       mapping_service: MappingService = Depends(MappingService)):
    try:
        mappings: list[MappingModel] = mapping_service.get_device_mappings(topology_id, group_id)
        return JSONResponse(content=jsonable_encoder(mappings), status_code=status.HTTP_200_OK)
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="topology_id has invalid format")
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
