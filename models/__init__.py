#!/usr/bin/python3
"""
initialize the models package
"""

from os import getenv


storage_t = getenv("HBNB_TYPE_STORAGE")

if storage_t == "db":
    from models.engine.db_storage import DBStorage, classes
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage, classes
    storage = FileStorage()
storage.reload()
