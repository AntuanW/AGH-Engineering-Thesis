from fastapi import FastAPI
from app.routes import api_routes

app = FastAPI()
app.include_router(api_routes.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
