from pydantic import BaseModel, Field
from typing import List
from beanie import PydanticObjectId
from users import PublicUser
from datetime import datetime
from messages import Message


class ChatDB(BaseModel):  # How Chats are saved in the database
    deletion: datetime
    owner: PydanticObjectId
    users: List[PydanticObjectId]
    created: datetime


class Chat(BaseModel):  # How Chats are sent back from the API
    owner: PublicUser
    users: List[PublicUser]
    created: datetime


class FullChat(Chat):  # Sending back the chat with all the messages
    messages: List[Message]
