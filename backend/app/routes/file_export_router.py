from fastapi import APIRouter, File, status, HTTPException, Depends
from fastapi.responses import FileResponse

from app.repository.mapping_repository import MappingRepository
from app.student_instruction_export.student_instruction_export_service import StudentInstructionExportService
import os

router = APIRouter(prefix="/file_export")


@router.get("/export_student_instructions")
async def export_instructions(mapping_repository: MappingRepository = Depends(MappingRepository),
                              instruction_export_service: StudentInstructionExportService = Depends(
                                  StudentInstructionExportService)):
    """
    Returns a PDF file with instructions on how to connect devices in laboratory room.
    :return: PDF file
    """
    mappings = mapping_repository.find_objects({})
    filename = instruction_export_service.export_instructions(mappings)

    path = os.path.join("student_instruction_export/pdf_files", filename)
    return FileResponse(path, media_type='application/pdf', filename=filename)

