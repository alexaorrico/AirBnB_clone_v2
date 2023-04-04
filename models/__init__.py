#!/usr/bin/python3
"""
initialize the models package
"""

from os import getenv
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage


storage_t = getenv("HBNB_TYPE_STORAGE")

if storage_t == "db":
    classes = DBStorage.classes
    storage = DBStorage()
else:
    classes = FileStorage.classes
    storage = FileStorage()
storage.reload()
