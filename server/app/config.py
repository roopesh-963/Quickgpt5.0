import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = "quickgpt"

async def init_db(models):
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[DB_NAME]
    await init_beanie(database=db, document_models=models)
