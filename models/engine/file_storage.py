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

    def get(self, cls, id):
        """gets specific object
        cls: class
        id: id of object instance
        return: object or None
        """
        all_classes = self.all(cls)
        for obj in all_classes.values():
            if id == str(obj.id):
                return obj
        return None

    def count(self, cls=None):
        """returns count of an obj instances"""
        return len(self.all(cls))

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        json_objects = {}
        for key in self.__objects:
            json_objects[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """deserializes the JSON file to __objects"""
        f_name = FileStorage.__file_path
        FileStorage.__objects = {}
        try:
            with open(f_name, mode='r', encoding='utf-8') as file_io:
                new_objs = json.load(file_io)
        except FileNotFoundError:
            return
        for obj_id, d in new_objs.items():
            k_cls = d['__class__']
            d.pop("__class__", None)
            d["created_at"] = datetime.strptime(d["created_at"],
                                                "%Y-%m-%d %H:%M:%S.%f")
            d["updated_at"] = datetime.strptime(d["updated_at"],
                                                "%Y-%m-%d %H:%M:%S.%f")
            FileStorage.__objects[obj_id] = FileStorage.classes[k_cls](**d)

    def delete(self, obj=None):
        """delete obj from __objects if it’s inside"""
        if obj is None:
            return
        for k_l in list(FileStorage.__objects.keys()):
            if obj.id == k_l.split(".")[1] and k_l.split(".")[0] in str(obj):
                FileStorage.__objects.pop(k_l, None)
                self.save()

    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()
