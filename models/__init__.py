#!/usr/bin/python3
"""
initialize the models package
CNC - dictionary = { Class Name (string) : Class Type }
"""
from os import getenv


storage_t = getenv("HBNB_TYPE_STORAGE")

if storage_t == "db":
    from models.engine.db_storage import DBStorage
    CNC = DBStorage.CNC
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    CNC = FileStorage.CNC
    storage = FileStorage()

storage.reload()
