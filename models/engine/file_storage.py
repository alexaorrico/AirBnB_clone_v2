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

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        json_objects = {}
        for key in self.__objects:
            json_objects[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.__objects[key] = classes[jo[key]["__class__"]](**jo[key])
        except:
            pass

    def delete(self, obj=None):
        """delete obj from __objects if it’s inside"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]
    def get(self, cls, id):
        """Returns the object based on the class and its ID, or None if not found"""
        cls_name = cls if isinstance(cls, str) else cls.__name__
        if cls_name in classes:
            key = cls_name + "." + id
            return self.__objects.get(key, None) # This is used to retrieve key in dictionary else return None.
        return None 

    def count(self, cls=None):
        count = 0
        if cls is None:
            for key in self.__objects:
                count += 1
        else:
            cls_name = cls if isinstance(cls, str) else cls.__name__
            if cls_name in classes:
               for key in self.__objects:
                    key_cls_name = key.split('.')[0]
                    if cls_name is None or key_cls_name == cls_name:
                        count += 1
        return count
    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()
