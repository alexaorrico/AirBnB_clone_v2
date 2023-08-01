#!/usr/bin/python3
"""
initialize the models package
"""
import os
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

"""CNC - dictionary = { Class Name (string) : Class Type }"""

if os.environ.get('HBNB_TYPE_STORAGE') == 'db':
    from models.engine import db_storage
    classes = db_storage.DBStorage.classes
    storage = db_storage.DBStorage()
else:
    from models.engine import file_storage
    classes = file_storage.FileStorage.classes
    storage = file_storage.FileStorage()

storage.reload()

#import os

#storage_t = os.environ.get("HBNB_TYPE_STORAGE")

#if storage_t == "db":
#    from models.engine import db_storage
#    classes = db_storage.DBStorage.classes
#    storage = db_storage.DBStorage()
#else:
#    from models.engine import file_storage
#    classes = file_storage.FileStorage.classes
#   storage = file_storage.FileStorage()
#storage.reload()
