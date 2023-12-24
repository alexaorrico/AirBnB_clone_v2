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
    """Serializes instances to a JSON file & deserializes back to instances"""

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Returns the dictionary __objects"""
        return {
            key: value for key, value in self.__objects.items()
            if cls == value.__class__ or cls == value.__class__.__name__
        } if cls else self.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            self.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)"""
        json_objects = {key: obj.to_dict() for key,
                        obj in self.__objects.items()}
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key, value in jo.items():
                cls_name = value["__class__"]
                self.__objects[key] = classes[cls_name](**value)
        except Exception:
            pass

    def delete(self, obj=None):
        """Delete obj from __objects if it’s inside"""
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            self.__objects.pop(key, None)

    def close(self):
        """Call reload() method for deserializing the JSON file to objects"""
        self.reload()

    def get(self, cls, id):
        """Retrieve one object"""
        key = f"{cls.__name__}.{id}"
        return self.__objects.get(key, None)

    def count(self, cls=None):
        """Count the number of objects in storage"""
        return len(self.__objects) if not cls else len([
            obj for obj in self.__objects.values() if isinstance(obj, cls)
        ])
