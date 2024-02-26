#!/usr/bin/python3
"""
initialize the models package
"""

from os import getenv


storage_t = getenv("HBNB_TYPE_STORAGE")

if storage_t == "db":
    from models.engine import db_storage
    storage = db_storage.DBStorage()
    classes = db_storage.classes
else:
    from models.engine import file_storage
    storage = file_storage.FileStorage()
    classes = file_storage.classes
storage.reload()
