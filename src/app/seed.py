import argparse
from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import UUID, uuid5

from app.config import Settings
from app.database import Database

SEED_NAMESPACE = "4b6d2f94-70ae-4cc8-9c9e-f0e2e1e8a1e0"
STORE_NAMES = ["Central Market", "North Point", "West End", "River Mall", "Airport Plaza"]
CITY_NAMES = ["Kyiv", "Lviv", "Odesa", "Dnipro", "Kharkiv"]
DEPARTMENT_NAMES = ["Electronics", "Food", "Clothing", "Household", "Sports"]
DEPARTMENTS_PER_STORE = [2, 4, 1, 3, 5]
FIRST_NAMES = ["Anna", "John", "Maria", "Peter", "Olena", "Mark"]
LAST_NAMES = ["Smith", "Brown", "Wilson", "Miller", "Taylor", "Johnson"]
POSITIONS = ["Manager", "Cashier", "Consultant", "Warehouse worker"]


def make_id(value: str) -> str:
    return str(uuid5(UUID(SEED_NAMESPACE), value))


def build_documents() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    now = datetime.now(timezone.utc)
    stores: list[dict[str, Any]] = []
    sellers: list[dict[str, Any]] = []
    seller_number = 0

    for store_index, store_name in enumerate(STORE_NAMES):
        store_id = make_id(f"store-{store_index}")
        departments = []
        department_count = DEPARTMENTS_PER_STORE[store_index]

        for department_index, department_name in enumerate(DEPARTMENT_NAMES[:department_count]):
            department_id = make_id(f"department-{store_index}-{department_index}")
            department_created_at = now - timedelta(
                days=store_index * 30 + department_index * 6 + 2
            )
            departments.append(
                {
                    "id": department_id,
                    "name": department_name,
                    "floor": department_index + 1,
                    "description": f"{department_name} department of {store_name}.",
                    "created_at": department_created_at,
                    "updated_at": department_created_at
                    + timedelta(days=(store_index + department_index) % 4),
                }
            )

            sellers_in_department = 2 + ((store_index * 2 + department_index * 3) % 7)
            for _ in range(sellers_in_department):
                sellers.append(
                    {
                        "_id": make_id(f"seller-{seller_number}"),
                        "first_name": FIRST_NAMES[seller_number % len(FIRST_NAMES)],
                        "last_name": LAST_NAMES[seller_number % len(LAST_NAMES)],
                        "age": 20 + seller_number % 41,
                        "phone": f"+38050{seller_number:07d}",
                        "email": f"seller{seller_number}@example.com",
                        "position": POSITIONS[seller_number % len(POSITIONS)],
                        "salary": float(800 + (seller_number % 8) * 125),
                        "store_id": store_id,
                        "department_id": department_id,
                        "created_at": now - timedelta(days=seller_number),
                        "updated_at": now - timedelta(days=seller_number // 2),
                    }
                )
                seller_number += 1

        stores.append(
            {
                "_id": store_id,
                "name": store_name,
                "address": {
                    "city": CITY_NAMES[store_index],
                    "street": f"Main Street {store_index + 1}",
                    "building": str(10 + store_index),
                },
                "contact_phone": f"+38044{store_index:07d}",
                "is_active": store_index != 4,
                "departments": departments,
                "departments_count": len(departments),
                "created_at": now - timedelta(days=store_index * 30),
                "updated_at": now - timedelta(days=store_index * 10),
            }
        )

    return stores, sellers


def seed(reset: bool = False) -> None:
    settings = Settings()
    database = Database(settings.mongo_uri, settings.mongo_database)

    try:
        database.connect()
        database.create_indexes()
        stores_collection = database.database["stores"]
        sellers_collection = database.database["sellers"]

        if reset:
            sellers_collection.delete_many({})
            stores_collection.delete_many({})

        stores, sellers = build_documents()
        for document in stores:
            stores_collection.replace_one({"_id": document["_id"]}, document, upsert=True)
        for document in sellers:
            sellers_collection.replace_one({"_id": document["_id"]}, document, upsert=True)

        department_count = sum(len(store["departments"]) for store in stores)
        print(f"Seeded {len(stores)} stores, {department_count} departments,")
        print(f"and {len(sellers)} sellers into '{settings.mongo_database}'.")
    finally:
        database.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed MongoDB with demo store data.")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Delete existing stores and sellers before inserting seed data.",
    )
    args = parser.parse_args()
    seed(reset=args.reset)


if __name__ == "__main__":
    main()
