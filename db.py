import os
import motor.motor_asyncio
from fastapi_users.db import BeanieUserDatabase
from dotenv import load_dotenv
from models.users import User
from logger import logger
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
logger.debug(DATABASE_URL)
client = motor.motor_asyncio.AsyncIOMotorClient(
    DATABASE_URL, uuidRepresentation="standard"
)
db = client["rowmate"]

async def get_user_db():
    yield BeanieUserDatabase(User)
