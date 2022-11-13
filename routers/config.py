from fastapi import APIRouter
from typing import Optional
from fastapi import Query
import pydantic
from fastapi.encoders import jsonable_encoder
from config import config
from models.config import Config


router = APIRouter(
    prefix="/config",
    tags=["boat"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=Config)
def get_config():
    return config
