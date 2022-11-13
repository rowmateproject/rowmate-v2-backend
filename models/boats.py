from bson import ObjectId
from pydantic import BaseModel, Field


class Boat(BaseModel):
    name: str


class CreateBoat(BaseModel):
    name: str = Field(None, max_length=100)