from fastapi_users import schemas
from fastapi_users.db import BeanieBaseUser
from pydantic import BaseModel, Field, EmailStr, validator
from typing import Literal, Dict, List
from beanie import PydanticObjectId
import string
import datetime
import json
from config import config

top = ("NoHair", "Eyepatch", "Hat", "Hijab", "Turban", "WinterHat1", "WinterHat2", "WinterHat3", "WinterHat4", "LongHairBigHair", "LongHairBob", "LongHairBun", "LongHairCurly", "LongHairCurvy", "LongHairDreads", "LongHairFrida", "LongHairFro", "LongHairFroBand", "LongHairNotTooLong", "LongHairShavedSides", "LongHairMiaWallace", "LongHairStraight", "LongHairStraight2", "LongHairStraightStrand", "ShortHairDreads01", "ShortHairDreads02", "ShortHairFrizzle", "ShortHairShaggyMullet", "ShortHairShortCurly", "ShortHairShortFlat", "ShortHairShortRound", "ShortHairShortWaved", "ShortHairSides", "ShortHairTheCaesar", "ShortHairTheCaesarSidePart")
topColor = ("Black", "Blue01", "Blue02", "Blue03", "Gray01", "Gray02", "Heather", "PastelBlue", "PastelGreen", "PastelOrange", "PastelRed", "PastelYellow", "Pink", "Red", "White")
accessories = ("Blank", "Kurt", "Prescription01", "Prescription02", "Round", "Sunglasses", "Wayfarers")
hairColor = ("Auburn", "Black", "Blonde", "BlondeGolden", "Brown", "BrownDark", "PastelPink", "Blue", "Platinum", "Red", "SilverGray")
facialHair = ("Blank", "BeardMedium", "BeardLight", "BeardMajestic", "MoustacheFancy", "MoustacheMagnum")
clothes = ("BlazerShirt", "BlazerSweater", "CollarSweater", "GraphicShirt", "Hoodie", "Overall", "ShirtCrewNeck", "ShirtScoopNeck", "ShirtVNeck")
eyes = ("Close", "Cry", "Default", "Dizzy", "EyeRoll", "Happy", "Hearts", "Side", "Squint", "Surprised", "Wink", "WinkWacky")
eyebrows = ("Angry", "AngryNatural", "Default", "DefaultNatural", "FlatNatural", "RaisedExcited", "RaisedExcitedNatural", "SadConcerned", "SadConcernedNatural", "UnibrowNatural", "UpDown", "UpDownNatural")
mouths = ("Concerned", "Default", "Disbelief", "Eating", "Grimace", "Sad", "ScreamOpen", "Serious", "Smile", "Tongue", "Twinkle", "Vomit")
skins = ("Tanned", "Yellow", "Pale", "Light", "Brown", "DarkBrown", "Black")
graphic = ("Bat", "Cumbia", "Deer", "Diamond", "Hola", "Pizza", "Resist", "Selena", "Bear", "SkullOutline", "Skull")

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


class User(BeanieBaseUser[PydanticObjectId]):
    is_accepted: bool
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
