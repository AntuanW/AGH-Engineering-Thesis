from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import api_routes
from running_config.BasicConfigExtractor import BasicConfigExtractor
import pprint

# app = FastAPI()
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "PUT", "DELETE"],
#     allow_headers=["*"]
# )
#
# app.include_router(api_routes.router)

if __name__ == "__main__":
    # import uvicorn
    xml_parser = BasicConfigExtractor()
    xml_parser.get_topology_config_from_xml(
        "C:\\Studia\\Informatyka_WIeIT\\Inzynierka\\AGH-Engineering-Thesis\\backend\\app\\running_config\\tmp_dir\\tracer822.xml")
    # uvicorn.run(app)
