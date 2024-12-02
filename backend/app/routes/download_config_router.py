from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse

from app.config_download.config_download_service import ConfigDownloadService
from app.config_download.dto.download_request_dto import DownloadConfigsDto

router = APIRouter(prefix="/config-download")

@router.post("/")
async def download_config(
        configs_download_info: DownloadConfigsDto,
      config_download_service: ConfigDownloadService = Depends(ConfigDownloadService)
) -> FileResponse:
    # TODO: exception handling and shit
    zip_archive_path: str = config_download_service.get_physical_configs(configs_download_info)
    return FileResponse(path=zip_archive_path, status_code=200)