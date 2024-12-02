from tempfile import tempdir
import os

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse

from app.config_download.config_download_service import ConfigDownloadService
from app.config_download.dto.download_request_dto import DownloadConfigsDto


router = APIRouter(prefix="/config-download", tags=["config-download"])

@router.post("/")
async def download_config(
        configs_download_info: DownloadConfigsDto,
        config_download_service: ConfigDownloadService = Depends(ConfigDownloadService)
) -> FileResponse:
    # TODO: exception handling and shit
    zip_archive_path = config_download_service.get_physical_configs(configs_download_info)
    zip_name = os.path.basename(zip_archive_path)
    return FileResponse(path=zip_archive_path, filename=zip_name, status_code=200)

@router.get("/download")
async def download_config():
    from zipfile import ZipFile
    import tempfile, os

    archive_name = "dupa.zip"
    tempdir_path = tempfile.mkdtemp()
    zip_path = os.path.join(tempdir_path, archive_name)
    zip_obj = ZipFile(zip_path, "w")

    dupa_filepath = os.path.join(tempdir, "dupa.txt")
    with open(dupa_filepath, "w") as f:
        f.write("dupa\ndupa")
    zip_obj.write(dupa_filepath, os.path.basename(dupa_filepath))
    zip_obj.close()
    return FileResponse(path=zip_path, filename="dupa.zip", status_code=200)
