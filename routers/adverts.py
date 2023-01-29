from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from fastapi import Query
import pydantic
from fastapi.encoders import jsonable_encoder
from models.adverts import Advert, CreateAdvert, CreateAdvertResponse, AdvertDB
from db import db
from beanie import PydanticObjectId
from models.users import User
from users import fastapi_users, RequireRole
from datetime import datetime

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

adverts = db.Adverts


router = APIRouter(
    prefix="/adverts",
    tags=["adverts"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[Advert])
async def read_adverts(user: User = Depends(RequireRole("User"))):
    pipeline = [
        {"$lookup": {
          "from": "Boats",
          "localField": "boat",
          "foreignField": "_id",
          "as": "boat"
        }},
        {"$lookup": {
            "from": "User",
            "localField": "owner",
            "foreignField": "_id",
            "as": "owner"
        }},
        {"$addFields": {"boat": {"$arrayElemAt": ["$boat", 0]}}},
        {"$addFields": {"owner": {"$arrayElemAt": ["$owner", 0]}}}
    ]

    adslist = await adverts.aggregate(pipeline).to_list(10000)
    return adslist


@router.post("/add")
async def create_advert(advert: CreateAdvert, user: User = Depends(RequireRole("User"))):
    advert = vars(advert)
    advert["created"] = datetime.now()
    advert["owner"] = ObjectId(user.id)

    ins = await adverts.insert_one(vars(AdvertDB(**advert)))
    return {"id": ins.inserted_id}
