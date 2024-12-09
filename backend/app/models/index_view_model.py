from pydantic import BaseModel


class IndexViewModel(BaseModel):
    XMLs: list[dict[str, str]]
    topologies: list[dict[str, str]]
    lab_groups: list[dict[str, str]]