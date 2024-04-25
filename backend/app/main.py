from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import api_routes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"]
)

app.include_router(api_routes.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
