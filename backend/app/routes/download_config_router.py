from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse, FileResponse

from app.config_download.dto.download_request_dto import ConfigDownloadDto

router = APIRouter(prefix="/config-download")

@router.post("/")
async def download_config():
    pass
