import logging

from bson.errors import InvalidId
from fastapi import APIRouter, File, UploadFile, status, HTTPException, Depends
from fastapi.responses import FileResponse, JSONResponse
from bson.objectid import ObjectId

from app.resources.FileService import FileService, FileType
from app.decryptor.decryptor_service import DecryptorService, PktDecryptor
from app.running_config.running_config_service import RunningConfigService
from app.repository.topology_repository import TopologyRepository
from app.repository.decrypted_xml_repository import DecryptedXMLRepository
from app.config_upload.config_upload_service import ConfigUploadService
from app.config_upload.exceptions.config_upload_exceptions import DeviceBuildError, DeviceConfigError, \
    DeviceConnectionError
from app.mapping.mapping_service import MappingService
from app.models.mapping import MappingModel

router = APIRouter(prefix="/config_upload")

# dependencies
file_service = FileService()
decryptor_service = DecryptorService(PktDecryptor(), file_service)


@router.post("/upload_pkt")
async def upload_pkt(file: UploadFile = File(...), force_overwrite: bool = False):
    """
    Uploads a PKT file to server. The file must have a .pkt extension.
    :param file: File object
    :param force_overwrite: Whether to overwrite an existing file with the same name
    :return: None
    """
    if not file.filename.endswith(".pkt"):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid file type")

    name = file_service.strip_name(file.filename)

    if file_service.check_file_exists(name, FileType.PKT) and not force_overwrite:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"File {name}.pkt already exists.")

    try:
        content = file.file.read()
        file_service.save_pkt(file.filename, content)

    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Error while reading file: {ex}")

    finally:
        await file.close()


@router.get("/decrypt_pkt")
def decrypt_pkt(name: str, force_overwrite: bool = False):
    """
    Decrypts a PKT file to XML and returns the content
    :param name: Name of the target PKT file (must be previously uploaded!).
                 The prefix without '.pkt' is enough.
    :param force_overwrite: Whether to overwrite an existing XML file with the same name
    :return: XML file

    CAUTION: THIS ENDPOINT CRASHES THE SWAGGER INTERFACE!!!
    The generated XMLs are huge, and it supposedly runs out of memory.
    Please use CURL for testing.
    """
    base_name = file_service.strip_name(name)

    if not file_service.check_file_exists(base_name, FileType.PKT):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"File {name}.pkt does not exist.")

    if file_service.check_file_exists(base_name, FileType.XML) and not force_overwrite:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"File {name}.xml already exists.")

    decryptor_service.decrypt_pkt(base_name)

    xml_path = file_service.get_path(base_name, FileType.XML)
    return FileResponse(xml_path)


@router.post("/extract_xml/{topology_id}")
async def extract_config(
        topology_id: str,
        running_config_service: RunningConfigService = Depends(RunningConfigService),
        topology_repository: TopologyRepository = Depends(TopologyRepository),
        decrypted_xml_repository: DecryptedXMLRepository = Depends(DecryptedXMLRepository)
) -> JSONResponse:
    try:
        topology_id = ObjectId(topology_id)
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
    return JSONResponse(content=response, status_code=status.HTTP_200_OK)


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

    topology = topology_repository.find_one({"_id": ObjectId(topology_id)})
    if not topology:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topology not found")

    try:
        devices = config_upload_service.build_netmiko_devices(topology.get('topology'))
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


@router.get("topologies/{topology_id}/mapping")
def get_device_mapping(topology_id: str, mapping_service: MappingService = Depends(MappingService)):
    try:
        mapping: MappingModel = mapping_service.get_device_mapping(topology_id)
        return JSONResponse(content=mapping.__dict__, status_code=status.HTTP_200_OK)
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="topology_id has invalid format")
