#!/usr/bin/python3
"""
This is module file_storage

This module defines one class FileStorage.
This class hadles saving the information in json in a file
"""

import models
import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"Amenity": Amenity, "BaseModel": BaseModel,
           "City": City,"Place": Place, "Review": Review,
           "State": State, "User": User}


class FileStorage:
    """
    Stores objects in a file in a json format

    **Class Attributes**
        __file_path: private, the path/to/file
        __objects: private, a dictionary of all the objects

    **Instance Attributes**
        __models_available: private, classes currently handled
    """
    __file_path = "file.json"
    if os.getenv("FS_TEST", "no") == "yes":
        __file_path = "test_file.json"
    __objects = {}

    def all(self, cls=None):
        """
        Returns the required objects

        **Arguments**
            cls: not required, a valid Class Name
        """
        if cls is None:
            return FileStorage.__objects
        else:
            result = {}
            for k, v in FileStorage.__objects.items():
                if v.__class__.__name__ == cls:
                    result[k] = v
            return result

    def new(self, obj):
        """
        Adds a new object to __objects

        **Arguments**
            obj: an object
        """
        if obj is not None:
            FileStorage.__objects[obj.id] = obj

    def save(self):
        """puts all the object to file after serializing them"""
        store = {}
        for k in FileStorage.__objects.keys():
            store[k] = FileStorage.__objects[k].to_json(True)
        with open(FileStorage.__file_path, mode="w+", encoding="utf-8") as fd:
            fd.write(json.dumps(store))

    def reload(self):
        """
        Restart from what is saved on file
        All errors will be silently skipped
        """
        FileStorage.__objects = {}
        try:
            with open(FileStorage.__file_path,
                      mode="r+", encoding="utf-8") as fd:
                temp = json.load(fd)
        except Exception as e:
            return
        for k in temp.keys():
            cls = temp[k].pop("__class__", None)
            if cls not in self.__models_available.keys():
                continue
            # call a good init function
            FileStorage.__objects[k] = self.__models_available[cls](**temp[k])

    def delete(self, obj=None):
        """Remove an object from the dictionary"""
        if obj:
            FileStorage.__objects.pop(obj.id, None)
            self.save()

    def close(self):
        """Close a session"""
        self.reload()

    def get(self, cls, id):
        """
        Retrieve one object

        Arguments:
            cls: string representing a class name
            id: string representing the object id

        Return:
           object of cls and id passed in argument
        """
        if cls not in classes.values():
            return None

        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if (value.id == id):
                return value

        return None

    def count(self, cls=None):
        """
        Number of objects in a certain class

        Arguments:
            cls: String representing a class name (default None)

        Return:
            number of objects in that class or in total.
            -1 if the class is not valid
        """
        all_class = classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(models.storage.all(clas).values())
        else:
            count = len(models.storage.all(cls).values())

        return count
