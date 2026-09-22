from collections.abc import Mapping
from typing import Any

from pymongo.collection import Collection

from app.common.mappers import map_document
from app.modules.store.schemas import StoreModel


class StoreRepository:
    def __init__(self, collection: Collection) -> None:
        self._collection = collection

    def create(self, document: Mapping[str, Any]) -> StoreModel:
        self._collection.insert_one(dict(document))
        created = self.get_by_id(str(document["_id"]))
        if created is None:
            raise RuntimeError("Store was inserted but could not be read back.")
        return created

    def get_by_id(self, store_id: str) -> StoreModel | None:
        document = self._collection.find_one({"_id": store_id})
        return None if document is None else map_document(document, StoreModel)

    def get_all(self) -> list[StoreModel]:
        documents = self._collection.find().sort([("name", 1)])
        return [map_document(document, StoreModel) for document in documents]

    def update(self, store_id: str, updates: Mapping[str, Any]) -> StoreModel | None:
        self._collection.update_one({"_id": store_id}, {"$set": dict(updates)})
        return self.get_by_id(store_id)

    def delete(self, store_id: str) -> bool:
        result = self._collection.delete_one({"_id": store_id})
        return result.deleted_count > 0
