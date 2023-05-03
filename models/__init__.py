#!/usr/bin/python3
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review
from models.engine import file_storage
from models.engine import db_storage
from os import getenv
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

<<<<<<< HEAD
if getenv('HBNB_TYPE_STORAGE', 'fs') == 'db':
    storage = db_storage.DBStorage()
else:
    storage = file_storage.FileStorage()
=======

if getenv("HBNB_TYPE_STORAGE") == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

classes = {"User": User, "BaseModel": BaseModel,
           "Place": Place, "State": State,
           "City": City, "Amenity": Amenity,
           "Review": Review}

>>>>>>> 0e125649dcfd402fd7b762fe147243315523b4f2
storage.reload()
