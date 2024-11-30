from .base_repository import BaseRepository


class DecryptedXMLRepository(BaseRepository[dict]):
    def get_collection(self):
        return self.db['decrypted_xml']

    def insert(self, xml_dict):
        return super().insert(xml_dict)
