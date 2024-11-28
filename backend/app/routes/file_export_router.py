from fastapi import APIRouter, File, status, HTTPException, Depends
from fastapi.responses import FileResponse, JSONResponse

from app.repository.mapping_repository import MappingRepository
from app.student_instruction_export.student_instruction_export_service import StudentInstructionExportService

router = APIRouter(prefix="/file_export")


@router.get("/export_student_instructions")
async def export_instructions(mapping_repository: MappingRepository = Depends(MappingRepository),
                              instruction_export_service: StudentInstructionExportService = Depends(
                                  StudentInstructionExportService)):
    """
    Returns a PDF file with instructions on how to connect devices in laboratory room.
    :return: PDF file
    """
    devices = mapping_repository.find_all()
    
    instruction_export_service.export_instructions(devices)
