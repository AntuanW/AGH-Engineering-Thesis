from fastapi import APIRouter, UploadFile, HTTPException, File
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/")
def read_root():
    return {"Hello": "World"}

@router.post("/upload-pkt-file")
def upload_pkt_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".pkt"):
        raise HTTPException(
            status_code=400,
            detail="File must be a .pkt file"
        )
    
    # Process a file

    return JSONResponse(
        status_code=200,
        content={"message": "File uploaded successfully"}
    )