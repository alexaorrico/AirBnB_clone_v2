#!/usr/bin/python3
"""
initialize the models package
"""
import models.get as get

from os import getenv

storage_t = getenv("HBNB_TYPE_STORAGE")
class_models = get.get_models()

if storage_t == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
