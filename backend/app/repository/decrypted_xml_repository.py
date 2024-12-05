from .base_repository import BaseRepository
from ..models.xml import XMLModel


class DecryptedXMLRepository(BaseRepository[XMLModel]):
    def get_collection(self):
        return self.db['decrypted_xml']

    def insert(self, xml: XMLModel):
        return super().insert(xml.model_dump())
