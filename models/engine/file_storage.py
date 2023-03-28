#!/usr/bin/python3
"""
FileStorage Module
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
    """
    A class to serialize instances to a JSON file and deserializes back to instances
    """
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
        """
        Returns the dictionary __objects or filtered by class name
        """
        if cls:
            new_dict = {}
            for key, value in self.__objects.items():
                if isinstance(value, cls):
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        """
        Sets in __objects the obj with key <obj class name>.id
        """
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """
        Serializes __objects to the JSON file (path: __file_path)
        """
        with open(self.__file_path, 'w') as f:
            json.dump({k: v.to_dict() for k, v in self.__objects.items()}, f)

    def reload(self):
        """
        Deserializes the JSON file to __objects
        """
        try:
            with open(self.__file_path, 'r') as f:
                json_dict = json.load(f)
                for key, value in json_dict.items():
                    class_name = value['__class__']
                    obj = self.classes[class_name](**value)
                    self.__objects[key] = obj
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        Deletes an object from __objects
        """
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            self.__objects.pop(key, None)

    def close(self):
        """
        Calls reload() method for deserializing the JSON file to objects
        """
        self.reload()

    def get(self, cls, id):
        """
        Retrieves an object by class name and id
        """
        if cls and id:
            for obj in self.all(cls).values():
                if obj.id == id:
                    return obj
        return None

    def count(self, cls=None):
        """
        Returns the number of objects in __objects
        """
        if cls:
            return len(self.all(cls))
        return len(self.__objects)