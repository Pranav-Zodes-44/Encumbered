import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
import pprint
from dotenv import load_dotenv
from services import dto

load_dotenv()
_mongostring = os.getenv('MONGO')
_client = AsyncIOMotorClient(_mongostring, server_api=ServerApi('1'))
db = _client.main

async def insert_one(document, collection: str):
    await db[collection].insert_one(document)

async def update_one(filter: dict, new_value: dict, collection: str):
    await db[collection].update_one(filter, {"$set": new_value}, upsert=True)

async def find_one(filter: dict, collection: str):
    document = await db[collection].find_one(filter)
    return document