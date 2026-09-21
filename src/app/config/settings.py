from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mongo_host: str = "localhost"
    mongo_port: int = 27017
    mongo_database: str = "lab1_mongodb"
    mongo_user: str | None = None
    mongo_password: str | None = None

    @property
    def mongo_uri(self) -> str:
        if self.mongo_user and self.mongo_password:
            return f"mongodb://{self.mongo_user}:{self.mongo_password}@{self.mongo_host}:{self.mongo_port}"

        return f"mongodb://{self.mongo_host}:{self.mongo_port}"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
