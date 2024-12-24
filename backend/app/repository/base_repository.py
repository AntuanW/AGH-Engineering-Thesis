import types
import typing
from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from .config import MONGODB_URI
from .exceptions.repository_exceptions import DatabaseException


T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    _instance = None
    _db = None

    def __new__(cls):
        # `cls` is the deriving class
        # If no instance of cls has been created yet, create it.
        # Otherwise, return that previous instance
        if cls._instance is None:
            cls._instance = super(BaseRepository, cls).__new__(cls)

            # If it's the first repository to be created, connect to the database
            if BaseRepository._db is None:
                try:
                    client = MongoClient(MONGODB_URI)
                    BaseRepository._db = client.get_database('agh-thesis')
                except ConnectionFailure as e:
                    raise DatabaseException(f'Cannot establish database, reason: {e}')

        # Add a pointer to DB connection to the instance of subclass
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

    def find(self, *args, **kwargs) -> list:
        return list(self.get_collection().find(*args, **kwargs))

    def find_objects(self, query) -> list[T]:
        return [self._collection_type.model_validate(x) for x in self.get_collection().find(query)]

    def find_one(self, *args, **kwargs) -> dict:
        return self.get_collection().find_one(*args, **kwargs)

    def find_object(self, query) -> T | None:
        result = self.get_collection().find_one(query)
        if result is None:
            return None
        return self._collection_type.model_validate(result)

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
