#!/usr/bin/env python
"""A module that that serializes instances to a JSON file and deserializes
JSON file to instances"""

import json
import os
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State

class FileStorage:
    __file_path = 'storage.json'
    __objects = {}

    def __init__(self):
        self.reload()

    def all(self, cls=None):
        if cls:
            return {k: v for k, v in self.__objects.items() if isinstance(v, cls)}
        else:
            return self.__objects

    def new(self, obj):
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        with open(self.__file_path, 'w') as f:
            json.dump({k: v.to_dict() for k, v in self.__objects.items()}, f)

    def reload(self):
        if os.path.exists(self.__file_path):
            with open(self.__file_path, 'r') as f:
                data = json.load(f)
                for k, v in data.items():
                    cls = eval(v['__class__'])
                    self.__objects[k] = cls(**v)

    def delete(self, obj=None):
        if obj:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            del self.__objects[key]
            self.save()

    def close(self):
        self.reload()

    def get(self, cls, id):
        key = "{}.{}".format(cls.__name__, id)
        return self.__objects.get(key)

    def count(self, cls=None):
        """ Counts the number of objects in storage """
        if cls:
            return len(self.all(cls))
        return len(self.all())
