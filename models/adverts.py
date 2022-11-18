from pydantic import BaseModel, Field
from typing import Optional
from beanie import PydanticObjectId
from models.users import PublicUser
from datetime import datetime
from models.boats import Boat


class AdvertDB(BaseModel):  # like saved in DB
    owner: PydanticObjectId
    created: datetime
    time: datetime
    boat: Optional[PydanticObjectId]
    text: Optional[str]

class Advert(BaseModel):
    owner: PublicUser
    created: datetime
    time: datetime
    boat: Optional[Boat]
    text: Optional[str]


class CreateAdvert(BaseModel):
    time: datetime
    boat: Optional[PydanticObjectId]
    text: str = Field(None, max_length=256)

class CreateAdvertResponse(Advert):
    pass
