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

    def get(self, cls, id):
        """Retrieves an object based on the class name and its ID.

        Checks the `__objects` dictionary for the object if it exists.

        Args:
            cls (str): String representing the class name(Place, User, Amenity)
            id: (str): UUID4 string representing the object ID.

        Returns:
            The object if it exists. None if cls or id is None or if the
            object does not exist.
        """
        if cls is None or cls not in classes or id is None or type(id) is not \
                str:
            return None
        return (self.__objects.get(cls + '.' + id, None))

    def count(self, cls=None):
        """Retrieves the number of total objects based on the class name.
        If no cls is specified, all cls objects total is returned.

        Checks the `__objects` dictionary for the object if it exists.

        Args:
            cls (str): String representing the class name(Place, User, Amenity)

        Returns:
            The number of object if it exists.
        """
        count = 0
        if cls is not None:
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    count += 1
        else:
            for key, value in self.__objects.items():
                count += 1

        return count

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
            json_objects[key] = self.__objects[key].to_dict(hide_pw=False)
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                jo[key]['hash_pw'] = False
                self.__objects[key] = classes[jo[key]["__class__"]](**jo[key])
        except:
            pass

    def delete(self, obj=None):
        """delete obj from __objects if it’s inside"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()
