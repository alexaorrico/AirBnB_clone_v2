#!/usr/bin/python3
"""This module instantiates an object of class FileStorage or DBStorage"""
import env
from models.engine.file_storage import FileStorage

if env.HBNB_TYPE_STORAGE == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    storage = FileStorage()

storage.reload()
