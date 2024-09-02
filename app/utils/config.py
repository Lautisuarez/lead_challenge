from pydantic_settings import BaseSettings
from app.db import PostgreSQLManager
from dotenv import load_dotenv
import os

load_dotenv('.env')
load_dotenv("VERSION")

class Settings(BaseSettings):
    VERSION: str = os.environ.get("VERSION", default="?.?.?")

    # Database Config
    POSTGRES_USER: str = os.environ.get("POSTGRES_USER", default="")
    POSTGRES_PSWD: str = os.environ.get("POSTGRES_PSWD", default="")
    POSTGRES_URL: str = os.environ.get("POSTGRES_URL", default="")
    POSTGRES_PORT: str = os.environ.get("POSTGRES_PORT", default="")
    POSTGRES_DB: str = os.environ.get("POSTGRES_DB", default="")
    db_manager: PostgreSQLManager = PostgreSQLManager({
        "dbname": POSTGRES_DB,
        "user": POSTGRES_USER,
        "password": POSTGRES_PSWD,
        "host": POSTGRES_URL,
        "port": POSTGRES_PORT
    })

settings = Settings()
