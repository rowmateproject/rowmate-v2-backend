from pydantic import BaseModel, Field
from typing import List
from beanie import PydanticObjectId
from users import PublicUser
from datetime import datetime


class Message(BaseModel):
    deletion: datetime
    message: str
    created: datetime
    sender: PydanticObjectId
    chat: PydanticObjectId
