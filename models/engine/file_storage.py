#!/usr/bin/python3
"""Contains the FileStorage class."""

import json
import models
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from hashlib import md5

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """Serialize instances to a JSON file & deserializes back to instances."""

    # string - path to the JSON file
    __file_path = "file.json"
    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
        """Return the dictionary __objects."""
        if cls is not None:
            return {
                key: value
                for key, value in self.__objects.items()
                if cls in [value.__class__, value.__class__.__name__]
            }
        return self.__objects

    def new(self, obj):
        """Set in __objects the obj with key <obj class name>.id."""
        if obj is not None:
            key = f"{obj.__class__.__name__}.{obj.id}"
            self.__objects[key] = obj

    def save(self):
        """Serialize __objects to the JSON file (path: __file_path)."""
        json_objects = {}
        for key in self.__objects:
            if key == "password":
                json_objects[key].decode()
            json_objects[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """Deserialize the JSON file to __objects."""
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.__objects[key] = classes[jo[key]["__class__"]](**jo[key])
        except Exception:
            pass

    def delete(self, obj=None):
        """Delete obj from __objects if it’s inside."""
        if obj is not None:
            key = f'{obj.__class__.__name__}.{obj.id}'
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """Call reload() method for deserializing the JSON file to objects."""
        self.reload()

    def get(self, cls, id):
        """Return the object based on the class name and its ID, or
        None if not found."""

        if cls not in classes.values():
            return None

        all_cls = models.storage.all(cls)
        return next((value for value in all_cls.values()
                    if (value.id == id)), None)

    def count(self, cls=None):
        """Count the number of objects in storage."""
        all_class = classes.values()

        return (
            len(models.storage.all(cls).values())
            if cls else sum(len(models.storage.all(clas).values())
                            for clas in all_class)
        )
