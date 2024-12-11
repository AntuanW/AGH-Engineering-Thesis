import tempfile
from pathlib import Path

from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import FileResponse

from app.repository.exceptions.repository_exceptions import DatabaseException
from app.repository.mapping_repository import MappingRepository
from app.instruction_export.instruction_export_service import InstructionExportService
import os

router = APIRouter(prefix="/file_export", tags=["pdf-export"])


@router.get("/export_student_instructions/{topology_id}")
async def export_instructions(topology_id: str,
                              mapping_repository: MappingRepository = Depends(MappingRepository),
                              instruction_export_service: InstructionExportService = Depends(
                                  InstructionExportService)):
    """
    Returns a PDF file with instructions on how to connect devices in laboratory room.
    :return: PDF file
    """
    try:
        mappings: list = mapping_repository.find_objects({"topology_id": topology_id})
        if not mappings:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There are no mappings in the database.")
    except DatabaseException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Something went wrong with database connection.")
    try:
        filename = instruction_export_service.export_instructions(mappings)
    except FileNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Failed to generate the PDF file. Error: {e}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to generate the PDF file. Error: {e}")

    path = Path(tempfile.gettempdir()) / "pdf_files" / filename
    if not os.path.exists(path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed to generate the PDF file.")

    return FileResponse(path, media_type='application/pdf', filename=filename)
