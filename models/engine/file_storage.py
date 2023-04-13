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

    def count(self, cls=None):
        """
        Returns the amount of objects
        are in 'self.__objects'.

        If 'cls' is not None, this method
        returns the amount of 'cls' instances
        in 'self.__objects'.

        If cls is invalid or 'self.__objects'"""
        if cls is None:
            return len(self.__objects)
        elif type(cls) == type:
            return len(self.all(cls))
        else:
            raise TypeError(f"'cls' must be a class or None. Got: {cls}")

    def get(self, cls, id):
        """
        Returns the (or an) object in self.__objects
        of type 'cls' and that has 'id' as its 'id'.

        This method just calls
        'return self.objects.get(cls.__name__ + id),
        since that's all it takes to get this to work
        for a dictionary, which has distinct keys.

        If an object with these descriptions isn't found,
        this method returns None.
        Just like the 'dict.get' method.
        """
        if not isinstance(cls, type):
            raise TypeError(f"'cls' should be a class. Got: {cls}")
        if not isinstance(id, str):
            raise TypeError(f"'id' should be a string. Got: {id}")
        return self.__objects.get(f"{cls.__name__}.{id}")

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
        except Exception:
            pass

    def delete(self, obj=None):
        """delete obj from __objects if it’s inside"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]


    def count(self, cls=None):
        """
        Method that returns the number of objects in storage matching the given class.
        If no class is passed, returns the count of all objects in storage
        """
        if cls is not None:
            return len(self.all(cls))
        else:
            return len(self.all())


    def get(self, cls, id):
        """
        Method that returns the object based on the class and its ID,
        or None if not found
        """
        if cls in classes.values() and id is not None:
            obj = self.all(cls)
            for key, val in obj.items():
                if val.id == id:
                    return val
        return None

    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()
