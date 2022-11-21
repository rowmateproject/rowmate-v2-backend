from pydantic import BaseModel, Field
from typing import Literal
from beanie import PydanticObjectId
from config import config


class CreateBoat(BaseModel):
    name: str = Field(None, max_length=100)
    category: Literal[tuple(config["boatCategories"])]
    total: int = Field(None, lt=100, gt=0)
    cox: bool


class Boat(CreateBoat):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")


class CreateBoatResponse(BaseModel):
    id: PydanticObjectId


class FindBoatByName(BaseModel):
    name: str = Field(None, max_length=100)
