from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import FileResponse
from bson import ObjectId

from app.repository.exceptions.repository_exceptions import DatabaseException
from app.repository.mapping_repository import MappingRepository
from app.student_instruction_export.student_instruction_export_service import StudentInstructionExportService
import os

router = APIRouter(prefix="/file_export")


@router.get("/export_student_instructions/{topology_id}")
async def export_instructions(topology_id: str,
                                mapping_repository: MappingRepository = Depends(MappingRepository),
                                instruction_export_service: StudentInstructionExportService = Depends(
                                StudentInstructionExportService)):
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

    filename = instruction_export_service.export_instructions(mappings)

    path = os.path.join("student_instruction_export/pdf_files", filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed to generate the PDF file.")

    return FileResponse(path, media_type='application/pdf', filename=filename)
