from pydantic import BaseModel, Field, field_serializer
from .mapped_device import MappedDeviceModel
from enum import Enum


class MappingType(str, Enum):
    CREATED_FROM_PKT = "CREATED_FROM_PKT"
    DOWNLOADED = "DOWNLOADED"


class MappingCollectionModel(BaseModel):
    name: str
    type: MappingType
    topology_id: str | None
    # noinspection PyDataclass
    mappings: dict[int, list[MappedDeviceModel]] = Field(default_factory=dict)

    @field_serializer("mappings")
    def serialize_mappings(self, mappings):
        """This is because MongoDB does not accept ints as keys"""
        return {str(k): v for k, v in mappings.items()}
