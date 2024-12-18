import os
import tempfile
from pathlib import Path

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import FileResponse

from app.config_download.config_download_service import ConfigDownloadService
from app.config_download.utils.download_config_request import DownloadConfigRequest
from app.config_download.utils.downloaded_config import DownloadedConfig
from app.instruction_export.home_instruction_export_service import HomeInstructionExportService
from app.pdf_generator.pdf_generator import PdfGenerator

router = APIRouter(prefix="/config_download", tags=["config-download"])


@router.post("/download_configs")
async def download_configs(
        download_request: DownloadConfigRequest,
        config_download_service: ConfigDownloadService = Depends(ConfigDownloadService),
        home_instruction_export_service: HomeInstructionExportService = Depends(HomeInstructionExportService)
):
    config_download_service.change_hostnames_and_cdp_timers(download_request.devices)

    download_results: list[DownloadedConfig] = config_download_service.download_devices_config(download_request)

    try:
        filename = home_instruction_export_service.export_instruction(download_results)
    except FileNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Failed to generate the PDF file. Error: {e}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to generate the PDF file. Error: {e}")

    path = Path(tempfile.gettempdir()) / PdfGenerator.PDF_OUTPUT_DIR / filename
    if not os.path.exists(path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PDF file not found.")

    return FileResponse(path, media_type='application/pdf', filename=filename)
