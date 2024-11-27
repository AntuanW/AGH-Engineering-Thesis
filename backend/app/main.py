from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import upload_config_router, devices_management_router, file_export_router

from app.logging_setup import setup_logging
from pathlib import Path

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"]
)

app.include_router(upload_config_router.router)
app.include_router(devices_management_router.router)
app.include_router(file_export_router.router)


LOG_CONFIG = Path(__file__).parent / 'logging.yaml'
setup_logging(LOG_CONFIG)

def start():
    import uvicorn
    uvicorn.run(app)

if __name__ == "__main__":
    start()
