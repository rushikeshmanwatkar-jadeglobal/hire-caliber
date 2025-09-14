from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import DOCUMENT_MODELS, settings


async def init_mongo():
    try:
        client = AsyncIOMotorClient(host=settings.DB_HOST, port=settings.DB_PORT)
        db = client[settings.DB_NAME]  # type: ignore
        await init_beanie(database=db, document_models=DOCUMENT_MODELS)
    except Exception as e:
        raise e
