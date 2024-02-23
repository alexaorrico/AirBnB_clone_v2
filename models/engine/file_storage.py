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

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """serializes instances to a JSON file & deserializes back to instances"""

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """returns the dictionary __objects"""
        if cls:
            new_dict = {}
            for key, value in self.__objects.items():
                if isinstance(value, cls):
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        json_dict = {}
        for key, value in self.__objects.items():
            json_dict[key] = value.to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(json_dict, f)

    def reload(self):
        """deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                json_dict = json.load(f)
            for key, value in json_dict.items():
                class_name = value['__class__']
                cls = classes[class_name]
                self.__objects[key] = cls(**value)
        except Exception as e:
            pass

    def delete(self, obj=None):
        """delete obj from __objects if it’s inside"""
        if obj:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()

    def get(self, cls, id):
        """Retrieve one object"""
        key = "{}.{}".format(cls.__name__, id)
        return self.__objects.get(key, None)

    def count(self, cls=None):
        """Count the number of objects in storage"""
        itm = [obj for obj in self.__objects.values() if isinstance(obj, cls)]
        if cls:
            return len(itm)
        else:
            return len(self.__objects)
