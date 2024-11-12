from fastapi import APIRouter, File, status, HTTPException, Depends
from fastapi.responses import FileResponse, JSONResponse

router = APIRouter(prefix="/file_export")

@router.get("/export_instructions")
async def export_instructions():
    """
    Returns a PDF file with instructions on how to connect devices in laboratory room.
    :return: PDF file
    """