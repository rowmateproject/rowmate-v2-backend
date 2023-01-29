from fastapi_users import schemas
from fastapi_users.db import BeanieBaseUser
from pydantic import BaseModel, Field, EmailStr, validator
from typing import Literal, Dict, List
from beanie import PydanticObjectId
import string
import datetime
import json
from config import top, accessories, hairColor, facialHair, clothes, eyes, eyebrows, mouths, skins, topColor, graphic, config


roles = ("Manager","Admin","User")
class Avatar(BaseModel):
    #  Avataaar Model
    is_circle: bool = True
    topType: Literal[top] = "NoHair"
    accessoriesType: Literal[accessories] = "Blank"
    hairColor: Literal[hairColor] = "Black"
    facialHairType: Literal[facialHair] = "Blank"
    clotheType: Literal[clothes] = "BlazerShirt"
    eyeType: Literal[eyes] = "Default"
    eyebrowType: Literal[eyebrows] = "Default"
    mouthType: Literal[mouths] = "Default"
    skinColor: Literal[skins] = "Light"
    topColor: Literal[topColor] = "Black"
    graphicType: Literal[graphic] = "Deer"
    facialHairColor: Literal[hairColor] = "Black"
    clotheColor: Literal[topColor] = "Black"
    circleColor: str = Field("6fb8e0", max_length=6, min_length=6)

    @validator('circleColor')
    def hex(cls, v, values, **kwargs):
        if not all(c in string.hexdigits for c in v):
            raise ValueError('Not Hex Value')
        return v


class PublicUser(BaseModel):
    _id: PydanticObjectId  # Problems with _id and id ???
    firstname: str
    lastname: str
    avatar: Avatar
    roles: List[Literal[roles]]
    lang: Literal[tuple(config['langs'])]


class RestrictedUser(PublicUser):
    is_accepted: bool
    is_email_verified: bool
    is_active: bool
    is_superuser: bool
    is_verified: bool
    email: str

class User(BeanieBaseUser[PydanticObjectId]):
    is_accepted: bool
    is_email_verified: bool
    firstname: str
    lastname: str
    yob: int
    avatar: Avatar
    roles: List[Literal[roles]]
    lang: Literal[tuple(config['langs'])]

    class Config:
        orm_mode = True


class UserRead(PublicUser):
    yob: int
    is_active: bool
    is_verified: bool
    is_email_verified: bool
    is_superuser: bool
    is_accepted: bool

    class Config:
        orm_mode = True


class UserCreate(schemas.CreateUpdateDictModel):
    email: EmailStr
    avatar: Avatar
    password: str
    yob: int = Field(None, gt=1900, lt=datetime.date.today().year)
    lang: Literal[tuple(config['langs'])]
    firstname: str = Field(None, max_length=50, min_length=1)
    lastname: str = Field(None, max_length=50, min_length=1)
    is_active: bool = Field(False, const=True)  # Don't allow writing flags in registration, but initialise
    is_superuser: bool = Field(False, const=True)
    is_verified: bool = Field(False, const=True)
    is_accepted: bool = Field(False, const=True)
    is_email_verified: bool = Field(False, const=True)
    roles: List = Field(["User"], const=True)


class UserUpdate(BaseModel):
    pass
