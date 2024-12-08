import types
import typing
from abc import ABC, abstractmethod
from typing import TypeVar, Type, Generic
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from .config import MONGODB_URI
from .exceptions.repository_exceptions import DatabaseException


T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    _instance = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BaseRepository, cls).__new__(cls)
            try:
                cls._instance.client = MongoClient(MONGODB_URI)
                BaseRepository._db = cls._instance.client.get_database('agh-thesis')
            except ConnectionFailure as e:
                raise DatabaseException(f'Cannot establish database, reason: {e}')

        cls._instance.db = BaseRepository._db

        # Retrieve the type variable used in the deriving class
        bases = types.get_original_bases(cls)
        cls._instance._collection_type = typing.get_args(bases[0])[0]
        return cls._instance

    @abstractmethod
    def get_collection(self):
        pass

    @abstractmethod
    def insert(self, document):
        result = self.get_collection().insert_one(document)
        return result.inserted_id

    def find(self, query) -> list:
        return list(self.get_collection().find(query))

    def find_objects(self, query) -> list[T]:
        return [self._collection_type(**x) for x in self.get_collection().find(query)]

    def find_one(self, query) -> dict:
        return self.get_collection().find_one(query)

    def find_object(self, query) -> T | None:
        result = self.get_collection().find_one(query)
        if result is None:
            return None
        return self._collection_type(**result)

    def update(self, query, update_values) -> int:
        result = self.get_collection().update_one(query, {"$set": update_values})
        return result.modified_count

    def upsert(self, query, new_value) -> int:
        result = self.get_collection().update_one(query, {"$set": new_value}, upsert=True)
        return result.upserted_id

    def delete(self, query) -> int:
        result = self.get_collection().delete_many(query)
        return result.deleted_count

    def delete_one(self, query) -> int:
        result = self.get_collection().delete_one(query)
        return result.deleted_count
