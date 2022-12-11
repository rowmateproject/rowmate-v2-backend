from pydantic import BaseModel, Field
from typing import List, Optional
from beanie import PydanticObjectId
from models.users import PublicUser
from datetime import datetime
from models.messages import Message
from models.adverts import Advert


class ChatDB(BaseModel):  # How Chats are saved in the database
    deletion: datetime
    owner: PydanticObjectId
    users: List[PydanticObjectId]
    advert: Optional[PydanticObjectId]
    created: datetime


class Chat(BaseModel):  # How Chats are sent back from the API
    owner: PublicUser
    users: List[PublicUser]
    advert: Advert
    created: datetime


class FullChat(Chat):  # Sending back the chat with all the messages
    messages: List[Message]
