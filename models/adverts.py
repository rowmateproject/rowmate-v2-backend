from pydantic import BaseModel
from typing import Optional
from beanie import PydanticObjectId
from users import PublicUser
from datetime import datetime
from boats import Boat


class Advert(BaseModel):
    owner: PublicUser
    created: datetime
    time: datetime
    boat: Optional[Boat]


