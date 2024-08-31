from decouple import config, Config, RepositoryEnv
from pydantic_settings import BaseSettings
from app.db import PostgreSQLManager

config = Config(RepositoryEnv(".env"))

class Settings(BaseSettings):
    POSTGRES_USER: str = config("POSTGRES_USER", default="")
    POSTGRES_PSWD: str = config("POSTGRES_PSWD", default="")
    POSTGRES_URL: str = config("POSTGRES_URL", default="")
    POSTGRES_PORT: str = config("POSTGRES_PORT", default="")
    POSTGRES_DB: str = config("POSTGRES_DB", default="")
    db_manager: PostgreSQLManager = PostgreSQLManager({
        "dbname": POSTGRES_DB,
        "user": POSTGRES_USER,
        "password": POSTGRES_PSWD,
        "host": POSTGRES_URL,
        "port": POSTGRES_PORT
    })

settings = Settings()
