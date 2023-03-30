#!/usr/bin/python3
"""
Contains the FileStorage class
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class FileStorage:
    """Serializes instances to a JSON file and deserializes back to instances."""

    __file_path = "file.json"
    __objects = {}

    classes = {
        "Amenity": Amenity,
        "BaseModel": BaseModel,
        "City": City,
        "Place": Place,
        "Review": Review,
        "State": State,
        "User": User
    }

    def all(self, cls=None):
        """Returns a dictionary of all objects or a specific class of objects."""
        if cls is None:
            return self.__objects

        return {k: v for k, v in self.__objects.items() if isinstance(v, cls)}

    def new(self, obj):
        """Adds a new object to the object dictionary."""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Serializes the object dictionary to a JSON file."""
        json_dict = {}
        for key, value in self.__objects.items():
            json_dict[key] = value.to_dict()

        with open(self.__file_path, 'w', encoding='utf-8') as f:
            json.dump(json_dict, f)

    def reload(self):
        """Deserializes the JSON file to the object dictionary."""
        try:
            with open(self.__file_path, 'r', encoding='utf-8') as f:
                json_dict = json.load(f)

            for key, value in json_dict.items():
                class_name = value["__class__"]
                self.__objects[key] = self.classes[class_name](**value)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes an object from the object dictionary."""
        if obj is None:
            return

        key = "{}.{}".format(type(obj).__name__, obj.id)
        self.__objects.pop(key, None)

    def close(self):
        """Deserializes the JSON file to the object dictionary."""
        self.reload()

    def get(self, cls, id):
        """Gets the string representing the class name and object ID """
        string_dict = self.all(cls)
        for key, value in string_dict.items():
            if key == cls.__name__ + "." + id:
                return value

    def count(self, cls=None):
        '''
           Count the number of objects in storage
        '''
        count = 0
        class_dict = self.all(cls)
        count = len(class_dict)
        return count
