#!/usr/bin/python3
"""create a unique FileStorage or DbStorage instance for your application"""
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from os import environ

sqlStorage = environ.get('HBNB_TYPE_STORAGE')

if sqlStorage == "db":
    storage = DBStorage()
else:
    storage = FileStorage()

storage.reload()
