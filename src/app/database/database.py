from pymongo import MongoClient
from pymongo.database import Database as MongoDatabase


class Database:
    def __init__(self, uri: str, database_name: str) -> None:
        self._client: MongoClient = MongoClient(uri, serverSelectionTimeoutMS=5000)
        self._database: MongoDatabase = self._client[database_name]

    @property
    def database(self) -> MongoDatabase:
        return self._database

    def connect(self) -> None:
        self._client.admin.command("ping")

    def create_indexes(self) -> None:
        self._database["stores"].create_index([("name", 1)])
        self._database["stores"].create_index([("departments.id", 1)])
        self._database["stores"].create_index([("departments.name", 1)])
        self._database["sellers"].create_index(
            [("store_id", 1), ("department_id", 1), ("last_name", 1), ("first_name", 1)]
        )

    def close(self) -> None:
        self._client.close()
