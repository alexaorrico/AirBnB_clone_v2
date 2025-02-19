#!/usr/bin/python3
"""
Contains the FileStorage class
"""

import json
import os
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

    # string - path to the JSON file
    __file_path = "file.json"
    # dictionary - empty but will store all objects by <class name>.id
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

    def get(self, cls, id):
        """returns the object with the given id and class"""
        if cls is not None and id is not None:
            key = cls.__name__ + "." + id
            if key in self.__objects:
                return self.__objects[key]
        return None
    
    def count(self, cls=None):
        """returns the number of objects in __objects"""
        if cls is not None:
            count = 0
            for key in self.__objects:
                if self.__objects[key].__class__ == cls:
                    count += 1
            return count
        return len(self.__objects)

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        json_objects = {}
        for key in self.__objects:
            json_objects[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """This method deserializes the JSON file and populates the
        "__objects" dictionary with objects stored in the JSON file."""

        if os.path.isfile(self.__file_path):
            with open(self.__file_path, "r") as file:
                objects_dict = json.load(file)
            for key, value in objects_dict.items():
                cls_name = value["__class__"]
                if cls_name == "BaseModel":
                    self.__objects[key] = BaseModel(**value)
                elif cls_name == "User":
                    self.__objects[key] = User(**value)
                elif cls_name == "State":
                    self.__objects[key] = State(**value)
                elif cls_name == "City":
                    self.__objects[key] = City(**value)
                elif cls_name == "Amenity":
                    self.__objects[key] = Amenity(**value)
                elif cls_name == "Place":
                    self.__objects[key] = Place(**value)
                elif cls_name == "Review":
                    self.__objects[key] = Review(**value)

    def delete(self, obj=None):
        """delete obj from __objects if it’s inside"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()
