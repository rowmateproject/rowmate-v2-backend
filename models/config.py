# Model for the config file config.json
from pydantic import BaseModel
from typing import List, Literal

supported_languages = ("de-CH", "fr-CH")  # Supported languages


class Config(BaseModel):
    messagesttl: int
    langs: List[Literal[supported_languages]]
