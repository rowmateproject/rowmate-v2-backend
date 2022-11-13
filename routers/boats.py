from fastapi import APIRouter
from typing import List
from fastapi import Query
import pydantic
from fastapi.encoders import jsonable_encoder
from models.boats import CreateBoat, Boat
from db import db
from bson.objectid import ObjectId
pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

boats = db.Boats

router = APIRouter(
    prefix="/boats",
    tags=["boat"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[Boat])
async def read_root():
    return await boats.find().to_list(10000)


@router.post("/add")
async def add_boat(boat: CreateBoat):
    await boats.insert_one(jsonable_encoder(boat))
    return
