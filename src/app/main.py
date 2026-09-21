from app.config import Settings
from app.database import Database


def main() -> None:
    settings = Settings()

    database = Database(uri=settings.mongo_uri, database_name=settings.mongo_database)

    try:
        database.connect()

        print("MongoDB connected!")
        print(f"Database: {settings.mongo_database}")

    finally:
        database.close()


if __name__ == "__main__":
    main()
