#!/usr/bin/python3
"""
This module defines the FileStorage class.
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

# A dictionary that maps class names to their respective classes
classes = {
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

    __file_path = "file.json"  # The path to the JSON file
    __objects = {}  # A dictionary to store all objects by class name and ID

    def all(self, cls=None):
        """
        This method returns the dictionary of objects.

        If the optional argument cls is provided, it returns a dictionary
        containing only the objects of the specified class.
        """
        if cls is not None:
            filtered_dict = {}
            for key, value in self.__objects.items():
                if value.__class__ == cls or value.__class__.__name__ == cls:
                    filtered_dict[key] = value
            return filtered_dict
        return self.__objects

    def new(self, obj):
        """
        This method sets the object in the __objects dictionary with
        the key <obj class name>.id
        """
        if obj is not None:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        """
        This method serializes __objects to the JSON file (path: __file_path)
        """
        json_dict = {}
        for key, obj in self.__objects.items():
            json_dict[key] = obj.to_dict()
        with open(self.__file_path, "w") as file:
            json.dump(json_dict, file)

    def reload(self):
        """
        This method deserializes the JSON file to __objects.
        """
        try:
            with open(self.__file_path, "r") as file:
                json_dict = json.load(file)
            for key, obj_dict in json_dict.items():
                class_name = obj_dict["__class__"]
                self.__objects[key] = classes[class_name](**obj_dict)
        except Exception:
            pass

    def delete(self, obj=None):
        """
        This method deletes an object from the __objects dictionary
        if it exists.
        """
        if obj is not None:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """
        This method calls the reload() method to deserialize
        the JSON file to objects.
        """
        self.reload()

    def get(self, cls, id):
        """
        This method retrieves an object based on its class name
        and ID.
        """
        for key, value in self.all(cls).items():
            if key == "{}.{}".format(cls.__name__, id):
                return value

    def count(self, cls=None):
        """
        This method returns the number of objects in the storage.

        If the optional argument cls is provided, it returns the
        number of objects of the specified class.
        """
        if cls is not None
