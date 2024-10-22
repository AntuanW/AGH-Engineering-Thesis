from abc import ABC, abstractmethod
from pymongo import MongoClient
from app.repository.config import MONGODB_URI


class BaseRepository(ABC):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BaseRepository, cls).__new__(cls)
            cls._instance.client = MongoClient(MONGODB_URI)
            cls._instance.db = cls._instance.client.get_database('agh-thesis')
            print("ajhsdfjkasfgafjkahfgaf")
        print("to powinno byc 2 razy")
        return cls._instance

    @abstractmethod
    def get_collection(self):
        pass

    def find(self, query):
        return list(self.get_collection().find(query))

    def insert(self, document):
        result = self.get_collection().insert_one(document)
        return str(result.inserted_id)

    def update(self, query, update_values):
        result = self.get_collection().update_one(query, {"$set": update_values})
        return result.modified_count

    def delete(self, query):
        result = self.get_collection().delete_one(query)
        return result.deleted_count