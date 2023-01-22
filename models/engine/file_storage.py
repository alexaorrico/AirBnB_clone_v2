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
              #  cls in (value.__class__, value.__class__.__name__)
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
        for key in self.__objects.items():
            json_objects[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w', encoding='utf-8') as my_file:
            json.dump(json_objects, my_file)

    def reload(self):
        """deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r', encoding='utf-8') as my_file:
                js_load= json.load(my_file)
            for key in js_load:
                self.__objects[key] = classes[js_load[key]["__class__"]](**js_load[key])
        # except BaseException:
        except FileNotFoundError as error:
            print(error)

    def delete(self, obj=None):
        """delete obj from __objects if it’s inside"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """call reload() method for deserializing the JSON fil    e to objects"""
        self.reload()

    def get(self, cls, my_id):
        """
        Returns the object based on the class name and its ID, or None if not
        found
        """
        key = (f"{cls}.{my_id}")
        for key in self.__objects.items():
            return self.__objects[key]
        return None

    def count(self, cls=None):
        """
        Returns the number of objects in storage matching the given class name.
        If no name is passed, returns the count of all objects in storage.
        """
        if cls:
            counter = 0
            for obj in self.__objects.values():
                if obj.__class__.__name__ == cls:
                    counter += 1
            return counter
        return len(self.__objects)
