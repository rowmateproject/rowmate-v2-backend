from fastapi import APIRouter, Depends, HTTPException
from typing import List
from beanie import PydanticObjectId
from fastapi import Query
import pydantic
from fastapi.encoders import jsonable_encoder
from models.boats import CreateBoat, Boat, CreateBoatResponse, FindBoatByName
from db import db
from bson.objectid import ObjectId
from models.users import User, PublicUser
from users import fastapi_users, RequireRole
pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

users = db.User


def read_users_me():
    print(fastapi_users.current_user(active=True))
    return fastapi_users.current_user(active=True)


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/public/{id}", response_model=PublicUser)
async def public_user_by_id(id: PydanticObjectId, user: User = Depends(RequireRole("User"))):
    res = await users.find_one({"_id": id})
    res["id"] = res["_id"]
    return res

