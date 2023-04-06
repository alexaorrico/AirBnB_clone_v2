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

    def all(self, cls=None):
        """returns the dictionary __objects"""
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON"""
        json_objects = {}
        for key in self.__objects:
            json_objects[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """deserializes the JSON file"""
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.__objects[key] = classes[jo[key]["__class__"]](**jo[key])
        except Exception:
            pass

    def delete(self, obj=None):
        """delete objects"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """call reload()"""
        self.reload()

    def get(self, cls, id):
        """
         brings back the object with the type and ID specified, or None if the object cannot be located
        """
        if cls is None or id is None:
            return None
        else:
            all_obj = self.all(cls)
            for obj in all_obj.values():
                if obj.id == id:
                    return obj
            return None

    def count(self, cls=None):
        """
            count of all objects in storage        """
        return len(self.all(cls))