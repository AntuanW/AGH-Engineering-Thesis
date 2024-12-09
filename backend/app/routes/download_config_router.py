from fastapi import APIRouter, Depends, status
from fastapi.responses import FileResponse, JSONResponse, Response

from app.config_download.config_download_service import ConfigDownloadService
from app.config_download.utils.download_config_request import DownloadConfigRequest
from app.config_download.utils.downloaded_config import DownloadedConfig


router = APIRouter(prefix="/config_download", tags=["config-download"])


@router.post("/download_configs")
async def download_configs(
        download_request: DownloadConfigRequest,
        config_download_service: ConfigDownloadService = Depends(ConfigDownloadService)
):
    config_download_service.change_hostnames_and_cdp_timers(download_request.devices)

    download_results: list[DownloadedConfig] = config_download_service.download_devices_config(download_request)

    # TODO: reversed mapping to some packet tracer device
    # ...
    # TODO: pdf generation and preparing the file to download
    # return type will be changed after the above changes
    return Response(status_code=status.HTTP_204_NO_CONTENT)
