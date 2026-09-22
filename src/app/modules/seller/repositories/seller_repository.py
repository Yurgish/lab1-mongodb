from collections.abc import Mapping
from typing import Any

from pymongo.collection import Collection

from app.common.mappers import map_document
from app.modules.seller.schemas import SellerModel


class SellerRepository:
    def __init__(self, collection: Collection) -> None:
        self._collection = collection

    def create(self, document: Mapping[str, Any]) -> SellerModel:
        self._collection.insert_one(dict(document))
        created = self.get_by_id(str(document["_id"]))
        if created is None:
            raise RuntimeError("Seller was inserted but could not be read back.")
        return created

    def get_by_id(self, seller_id: str) -> SellerModel | None:
        document = self._collection.find_one({"_id": seller_id})
        return None if document is None else map_document(document, SellerModel)

    def get_all(self) -> list[SellerModel]:
        documents = self._collection.find().sort(
            [("store_id", 1), ("last_name", 1), ("first_name", 1)]
        )
        return [map_document(document, SellerModel) for document in documents]

    def get_by_department(self, store_id: str, department_id: str) -> list[SellerModel]:
        documents = self._collection.find(
            {"store_id": store_id, "department_id": department_id}
        ).sort([("last_name", 1), ("first_name", 1)])
        return [map_document(document, SellerModel) for document in documents]

    def update(self, seller_id: str, updates: Mapping[str, Any]) -> SellerModel | None:
        self._collection.update_one({"_id": seller_id}, {"$set": dict(updates)})
        return self.get_by_id(seller_id)

    def delete(self, seller_id: str) -> bool:
        result = self._collection.delete_one({"_id": seller_id})
        return result.deleted_count > 0

    def delete_by_store_id(self, store_id: str) -> int:
        result = self._collection.delete_many({"store_id": store_id})
        return result.deleted_count

    def delete_by_department_id(self, store_id: str, department_id: str) -> int:
        result = self._collection.delete_many(
            {"store_id": store_id, "department_id": department_id}
        )
        return result.deleted_count
