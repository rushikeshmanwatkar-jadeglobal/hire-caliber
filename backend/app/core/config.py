from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    MONGO_CONNECTION_STRING: Optional[str] = "mongodb://127.0.0.1:27017/hire_caliber"
    AZURE_OPENAI_API_KEY: Optional[str] = (
        "5bKI58jSZBaHLSWY5DS6fwyIqlEPtTIKqHi9tPdoUZOULfUqr7LmJQQJ99AKACHYHv6XJ3w3AAAAACOGyFpk"
    )
    AZURE_OPENAI_ENDPOINT: Optional[str] = (
        "https://hrish-m3zpdd19-eastus2.cognitiveservices.azure.com/"
    )
    OPENAI_API_VERSION: Optional[str] = "2024-02-01"
    EMBEDDING_MODEL_NAME: str = "hackathon-em-group5"
    CHAT_MODEL_NAME: str = "hackathon-group5"

    DB_NAME: Optional[str] = "hire_caliber"
    DB_USER: Optional[str] = None
    DB_PASSWORD: Optional[str] = None
    DB_HOST: Optional[str] = "localhost"
    DB_PORT: Optional[int] = 27017
    CHROMA_HTTP_HOST: str = "localhost"
    CHROMA_HTTP_PORT: int = 8000
    CELERY_BROKER_URL: str = ""
    CELERY_RESULT_BACKEND: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# class Settings(BaseSettings):
#     MONGO_CONNECTION_STRING: str = os.getenv("MONGO_CONNECTION_STRING") if os.getenv("MONGO_CONNECTION_STRING") else ""  # type: ignore
#     AZURE_OPENAI_API_KEY: str = os.getenv("AZURE_OPENAI_API_KEY") if os.getenv("AZURE_OPENAI_API_KEY") else ""  # type: ignore
#     AZURE_OPENAI_ENDPOINT: str = os.getenv("AZURE_OPENAI_ENDPOINT") if os.getenv("AZURE_OPENAI_ENDPOINT") else ""  # type: ignore
#     OPENAI_API_VERSION: str = os.getenv("OPENAI_API_VERSION") if os.getenv("OPENAI_API_VERSION") else ""  # type: ignore
#     EMBEDDING_MODEL_NAME: str = os.getenv("EMBEDDING_MODEL_NAME") if os.getenv("EMBEDDING_MODEL_NAME") else "hackathon-em-group5"  # type: ignore
#     CHAT_MODEL_NAME: str = os.getenv("CHAT_MODEL_NAME") if os.getenv("CHAT_MODEL_NAME") else "hackathon-group5"  # type: ignore
#     # Database settings
#     DB_NAME: Optional[str] = "hire_caliber"
#     DB_USER: Optional[str] = None
#     DB_PASSWORD: Optional[str] = None
#     DB_HOST: Optional[str] = (
#         os.getenv("DB_HOST") if os.getenv("DB_HOST") else "localhost"
#     )
#     DB_PORT: Optional[int] = os.getenv("DB_PORT") if os.getenv("DB_PORT") else 27017  # type: ignore
#     CHROMA_HTTP_HOST: str = "localhost"
#     CHROMA_HTTP_PORT: int = 8000
#     CELERY_BROKER_URL: str = ""
#     CELERY_RESULT_BACKEND: str = ""

#     class Config:
#         env_file = "../.env"
#         case_sensitive = True


# settings = Settings()  # type: ignore

DOCUMENT_MODELS = [
    "app.db.models.Job",
    "app.db.models.Candidate",
]
