from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import api_routes

from logging_setup import setup_logging
from pathlib import Path

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"]
)

app.include_router(api_routes.router)


LOG_CONFIG = Path(__file__).parent / 'logging.yaml'
setup_logging(LOG_CONFIG)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
