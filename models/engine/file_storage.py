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
            json_objects[key] = self.__objects[key].to_dict(True)
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f, indent=2)

    def reload(self):
        """deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.__objects[key] = classes[jo[key]["__class__"]](**jo[key])
        except FileNotFoundError:
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

    def get(self, cls, id):
        """
        Retrieves an object with given `id` from the file storage

        Args:
            cls (class): class of object to retrieve
            id (str): id of object to retrieve

        Returns:
            `obj` based on `cls and `id``, or None if not found
        """
        if cls not in classes and cls not in classes.values():
            raise TypeError("{} is not a valid class type".format(cls))

        if type(id) != str:
            raise TypeError("id must be a string")

        return next((obj for obj in self.all(cls).values() if obj.id == id),
                    None)

    def count(self, cls=None):
        """
        Returns the number of objects in file storage

        Args:
            cls (class): optional class of objects to count

        Returns:
            Count of objects belonging to `cls` in storage,
                or count of all objects if `cls` is None.
        """
        if cls is None:
            return len(self.all().values())

        if cls not in classes and cls not in classes.values():
            raise TypeError("{} is not a valid class type".format(cls))

        if type(cls) == str:
            cls = classes[cls]

        return len(self.all(cls).values())
