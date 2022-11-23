import json
from logger import logger

with open("config.json","r") as fobj:
    config = json.load(fobj)
    logger.info("Loaded config from config.json")