import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


def get_db_uri() -> str:
    return f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


SECRET_KEY = os.getenv("SECRET_KEY")
REFRESH_TOKEN_SECRET = os.getenv("REFRESH_TOKEN_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_EXPIRATION = timedelta(minutes=int(os.getenv("JWT_EXPIRATION"))) # type: ignore
REFRESH_TOKEN_SECRET_EXPIRATION = timedelta(
    minutes=int(os.getenv("REFRESH_TOKEN_SECRET_EXPIRATION")) # type: ignore
)

