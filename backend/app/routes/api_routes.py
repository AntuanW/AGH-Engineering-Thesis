from fastapi import APIRouter, File, UploadFile, status, HTTPException
from fastapi.responses import FileResponse
from backend.app.resources.FileService import FileService, FileType
from backend.app.decryptor.DecryptorService import DecryptorService, PktDecryptor

router = APIRouter()
file_service = FileService()
decryptor_service = DecryptorService(PktDecryptor(), file_service)

@router.get("/")
def read_root():
    return {"Hello": "World"}


@router.post("/upload_pkt")
async def upload_pkt(file: UploadFile = File(...), force_overwrite: bool = False):
    """
    Uploads a PKT file to server. The file must have a .pkt extension.
    :param file: File object
    :param force_overwrite: Whether to overwrite an existing file with the same name
    :return: None
    """
    if not file.filename.endswith(".pkt"):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid file type")

    name = file_service.strip_name(file.filename)

    if file_service.check_file_exists(name, FileType.PKT) and not force_overwrite:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"File {name}.pkt already exists.")

    try:
        content = file.file.read()
        file_service.save_pkt(file.filename, content)

    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Error while reading file: {ex}")

    finally:
        await file.close()


@router.get("/decrypt_pkt")
def decrypt_pkt(name: str, force_overwrite: bool = False):
    """
    Decrypts a PKT file to XML and returns the content
    :param name: Name of the target PKT file (must be previously uploaded!).
                 The prefix without '.pkt' is enough.
    :param force_overwrite: Whether to overwrite an existing XML file with the same name
    :return: XML file

    CAUTION: THIS ENDPOINT CRASHES THE SWAGGER INTERFACE!!!
    The generated XMLs are huge, and it supposedly runs out of memory.
    Please use CURL for testing.
    """
    base_name = file_service.strip_name(name)

    if not file_service.check_file_exists(base_name, FileType.PKT):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"File {name}.pkt does not exist.")

    if file_service.check_file_exists(base_name, FileType.XML) and not force_overwrite:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"File {name}.xml already exists.")

    decryptor_service.decrypt_pkt(base_name)

    xml_path = file_service.get_path(base_name, FileType.XML)
    return FileResponse(xml_path)