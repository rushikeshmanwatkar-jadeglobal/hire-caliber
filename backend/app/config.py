from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    MONGO_CONNECTION_STRING: str = (
        "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.5.1"
    )
    AZURE_OPENAI_API_KEY: str = (
        "5bKI58jSZBaHLSWY5DS6fwyIqlEPtTIKqHi9tPdoUZOULfUqr7LmJQQJ99AKACHYHv6XJ3w3AAAAACOGyFpk"
    )
    AZURE_OPENAI_ENDPOINT: str = (
        "https://hrish-m3zpdd19-eastus2.cognitiveservices.azure.com/"
    )
    OPENAI_API_VERSION: str = "2024-02-01"
    EMBEDDINGS_DEPLOYMENT_NAME: str = "hackathon-em-group5"
    CHAT_DEPLOYMENT_NAME: str = "hackathon-group5"
    # Database settings
    DB_NAME: Optional[str] = "hire_caliber"
    DB_USER: Optional[str] = None
    DB_PASSWORD: Optional[str] = None
    DB_HOST: Optional[str] = os.getenv("DB_HOST")
    DB_PORT: Optional[int] = os.getenv("DB_PORT")  # type: ignore
    CHROMA_HTTP_HOST: Optional[str] = "localhost"
    CHROMA_HTTP_PORT: Optional[int] = 8000

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()  # type: ignore
