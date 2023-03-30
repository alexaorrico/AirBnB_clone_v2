#!/usr/bin/env python3
"""
Handles the reading and writing of JSON data for storing all class instances.
"""

import json
from datetime import datetime
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class FileStorage:
    """Handles long-term storage of all class instances"""
    __file_path = 'file.json'
    __objects = {}

    CNC = {
        'BaseModel': BaseModel,
        'Amenity': Amenity,
        'City': City,
        'Place': Place,
        'Review': Review,
        'State': State,
        'User': User
    }

    def all(self, cls=None):
        """Returns a dictionary of all objects"""
        if cls is None:
            return FileStorage.__objects
        else:
            objects_of_cls = {}
            for key, value in FileStorage.__objects.items():
                if value.__class__.__name__ == cls:
                    objects_of_cls[key] = value
            return objects_of_cls

    def new(self, obj):
        """Adds new object to __objects dictionary"""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Serializes __objects dictionary to a JSON file"""
        dictionary = {}
        for key, value in FileStorage.__objects.items():
            dictionary[key] = value.to_dict()
        with open(FileStorage.__file_path, mode="w", encoding="utf-8") as file:
            json.dump(dictionary, file)

    def reload(self):
        """Deserializes JSON data from file and populates __objects"""
        try:
            with open(FileStorage.__file_path, mode="r") as file:
                dictionary = json.load(file)
            for key, value in dictionary.items():
                cls_name = value['__class__']
                cls = FileStorage.CNC[cls_name]
                FileStorage.__objects[key] = cls(**value)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes an object from __objects"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            if key in FileStorage.__objects:
                del FileStorage.__objects[key]
                self.save()

    def get(self, cls, id):
        """Returns the object with given class name and ID"""
        if cls is not None and id is not None:
            objects = self.all(cls)
            for obj in objects.values():
                if obj.id == id:
                    return obj
        return None

    def count(self, cls=None):
        """Counts the number of objects in storage"""
        if cls is not None:
            return len(self.all(cls))
        else:
            return len(FileStorage.__objects)

    def delete_all(self):
        """Deletes all objects in storage"""
        FileStorage.__objects.clear()
        self.save()

    def close(self):
        """Reloads the objects"""
        self.reload()
