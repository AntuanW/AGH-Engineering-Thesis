from .base_repository import BaseRepository
from ..models.xml import XMLModel


class DecryptedXMLRepository(BaseRepository[XMLModel]):
    def get_collection(self):
        return self.db.get_collection("decrypted_xml")

    def insert(self, xml: XMLModel):
        return super().insert(xml.model_dump())

    def list_names(self):
        return [{"name": obj["name"], "_id": str(obj["_id"])}
            for obj in self.get_collection().find({}, {"name": 1})]

    def upsert(self, query, new_value) -> int:
        names = [x["name"] for x in self.list_names()]
        if new_value["name"] in names:
            return -1
        super().insert(new_value)