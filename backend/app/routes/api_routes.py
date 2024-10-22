from fastapi import APIRouter, File, UploadFile, status, Response

router = APIRouter()


@router.get("/")
def read_root():
    return {"Hello": "World"}


@router.post("/decrypt")
def decrypt_pkt(response: Response, file: UploadFile = File(...)):
    try:
        name = file.filename
        contents = file.file.read()


    except Exception as ex:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        response.body = {"message": f"Error while reading file: {ex}"}

    finally:
        file.close()
