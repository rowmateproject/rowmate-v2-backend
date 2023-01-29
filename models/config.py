# Model for the config file config.json
from pydantic import BaseModel
from typing import List, Literal, Dict

supported_languages = ("de-CH", "fr-CH", "en-GB")  # Supported languages
supported_boat_categories = ("racing", "cgig", "other")  # Supported boat categories


class Config(BaseModel):
    messagesttl: int
    langs: List[Literal[supported_languages]]
    boatCategories: List[Literal[supported_boat_categories]]
    advertTextMaxLength: int
    avatarConfig: Dict
