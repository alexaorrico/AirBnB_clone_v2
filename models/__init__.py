#!/usr/bin/python3
"""
initialize the models package
"""

from os import getenv

from dotenv import load_dotenv
ENV_FILE_PATH='/home/shortninja/alx_work/AirBnB_clone_v3/.env'
load_dotenv(ENV_FILE_PATH)

storage_t = getenv("HBNB_TYPE_STORAGE")

if storage_t == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
