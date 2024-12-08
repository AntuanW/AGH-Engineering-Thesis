from pydantic import BaseModel, Field
from datetime import datetime


class XMLModel(BaseModel):
    name: str
    creation_date: datetime = Field(default_factory=datetime.now)
    xml: dict