# Instead of reading .env in every file, we centralize configuration in one place.
# Whenever we need database settings, we can import settings.

import os
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[3]

load_dotenv(ROOT_DIR / ".env")


class Settings:

    DB_SERVER = os.getenv("DB_SERVER")
    DB_NAME = os.getenv("DB_NAME")
    DB_DRIVER = os.getenv("DB_DRIVER")
    DB_TRUSTED_CONNECTION = os.getenv("DB_TRUSTED_CONNECTION", "yes")
    API_URL = os.getenv("API_URL")
    MODEL_NAME = os.getenv("MODEL_NAME")
    API_KEY = os.getenv("API_KEY")
    COLLECTION_NAME = os.getenv("COLLECTION_NAME")
    CHAT_MODEL = os.getenv("CHAT_MODEL")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_API_URL = os.getenv("OPENAI_API_URL")
    OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME")

settings = Settings()
