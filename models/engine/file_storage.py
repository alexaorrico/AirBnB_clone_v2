#!/usr/bin/env python3
"""
This module contains the FileStorage class.
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

# Mapping of class names to their corresponding classes
CLASSES = {
    "Amenity": Amenity,
    "BaseModel": BaseModel,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User,
}


class FileStorage:
    """
    This class serializes instances to a JSON file and deserializes
    back to instances.
    """

    # Path to the JSON file
    __file_path = "file.json"
    # Dictionary to store all objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
        """
        Returns the dictionary __objects. If cls is not None, returns a
        new dictionary containing only objects of the specified class.
        """
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        """
        Sets the object in __objects with key <obj class name>.id
        """
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """
        Serializes __objects to the JSON file (path: __file_path).
        """
        json_objects = {}
        for key in self.__objects:
            json_objects[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """
        Deserializes the JSON file to __objects.
        """
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.__objects[key] = CLASSES[jo[key]["__class__"]](**jo[key])
        except Exception:
            pass

    def delete(self, obj=None):
        """
        Deletes obj from __objects if it's inside.
        """
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """
        Calls reload() method for deserializing the JSON file to objects.
        """
        self.reload()

    def get(self, cls, id):
        """
        Returns the object based on the class and its ID, or None if not found.
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
        Returns the number of objects in storage matching the given class.
        If no class is passed, returns the count of all objects in storage.
        """
        return len(self.all(cls))