#!/usr/bin/python3
"""
initialize the models package
"""

from os import getenv

storage_t = getenv("HBNB_TYPE_STORAGE")

if storage_t == "db":
    from models.engine.db_storage import DBStorage
    class_richard = DBStorage.class_richard
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    class_richard = FileStorage.class_richard
    storage = FileStorage()
storage.reload()
