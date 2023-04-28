from fastapi import APIRouter, Depends, HTTPException
from typing import List
from beanie import PydanticObjectId
from fastapi import Query
import pydantic
from fastapi.encoders import jsonable_encoder
from models.boats import CreateBoat, Boat, CreateBoatResponse, FindBoatByName
from db import db
from bson.objectid import ObjectId
from models.users import User
from users import fastapi_users, RequireRole
pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

boats = db.Boats


def read_users_me():
    print(fastapi_users.current_user(active=True))
    return fastapi_users.current_user(active=True)


router = APIRouter(
    prefix="/boats",
    tags=["boat"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[Boat])
async def read_boats(user: User = Depends(RequireRole("User"))):
    return await boats.find().to_list(10000)


@router.get("/{id}",response_model=Boat)
async def boat_by_id(id: PydanticObjectId, user: User = Depends(RequireRole("User"))):
    return await boats.find_one({"_id": id})


@router.post("/add", response_model=CreateBoatResponse)
async def add_boat(boat: CreateBoat, user: User = Depends(RequireRole("Admin"))):
    search = FindBoatByName()
    search.name = boat.name
    if await boats.find_one(jsonable_encoder(search)) is not None:
        raise HTTPException(409, detail="A boat with this name already exists")
    ins = await boats.insert_one(jsonable_encoder(boat))
    return {"id": ins.inserted_id}


@router.delete("/{id}", response_model=PydanticObjectId)
async def delete_boat(id: PydanticObjectId, user: User = Depends(RequireRole("Admin"))):
    res = await boats.delete_one({"_id": id})
    if res.deleted_count == 1:
        return id
    else:
        raise HTTPException(409, detail="Boat could not be deleted. Maybe it has already been deleted?")
