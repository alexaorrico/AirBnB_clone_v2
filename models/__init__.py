#!/usr/bin/python3
"""
initialize the models package
"""

from os import getenv
from models.engine import file_storage
from models.engine import db_storage


storage_t = getenv("HBNB_TYPE_STORAGE")

if storage_t == "db":
    storage = DBStorage()
else:
    storage = FileStorage()
storage.reload()
