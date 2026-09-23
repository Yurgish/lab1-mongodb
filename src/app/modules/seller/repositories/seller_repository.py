from collections.abc import Mapping
from typing import Any

from pymongo.collection import Collection

from app.common.mappers import map_document
from app.common.query import QueryOptions, get_sort_spec, text_search
from app.modules.seller.schemas import SellerModel

SELLER_SORT_FIELDS = {
    "last_name": "last_name",
    "first_name": "first_name",
    "position": "position",
    "salary": "salary",
    "age": "age",
    "email": "email",
    "created_at": "created_at",
    "updated_at": "updated_at",
}
SELLER_SEARCH_FIELDS = ("first_name", "last_name", "email", "position")


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

    def get_all(self, options: QueryOptions | None = None) -> list[SellerModel]:
        options = options or QueryOptions(sort_by="last_name")
        documents = self._collection.find(text_search(options.search, SELLER_SEARCH_FIELDS)).sort(
            get_sort_spec(options, SELLER_SORT_FIELDS)
        )
        return [map_document(document, SellerModel) for document in documents]

    def get_by_department(
        self, store_id: str, department_id: str, options: QueryOptions | None = None
    ) -> list[SellerModel]:
        options = options or QueryOptions(sort_by="last_name")
        query = {
            "store_id": store_id,
            "department_id": department_id,
            **text_search(options.search, SELLER_SEARCH_FIELDS),
        }
        documents = self._collection.find(query).sort(get_sort_spec(options, SELLER_SORT_FIELDS))
        return [map_document(document, SellerModel) for document in documents]

    def get_by_store(self, store_id: str, options: QueryOptions | None = None) -> list[SellerModel]:
        options = options or QueryOptions(sort_by="last_name")
        query = {"store_id": store_id, **text_search(options.search, SELLER_SEARCH_FIELDS)}
        documents = self._collection.find(query).sort(get_sort_spec(options, SELLER_SORT_FIELDS))
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

    def count_by_department(self, store_id: str, department_id: str) -> int:
        return self._collection.count_documents(
            {"store_id": store_id, "department_id": department_id}
        )
