from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
from app.schemas.db_models import Candidate, Job


async def initialize_database():
    """Initializes the MongoDB connection and Beanie ODM."""
    client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)
    db = client[settings.DB_NAME]  # type: ignore

    await init_beanie(database=db, document_models=[Candidate, Job])  # type: ignore
