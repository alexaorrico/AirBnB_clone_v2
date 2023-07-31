#!/usr/bin/python3
"""
Contains the FileStorage class usesed for I/O, writing and readng,
of JSON of all class instances
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

to_json = BaseModel.to_json

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """serializes instances to a JSON file & deserializes back to instances"""
    classes = {
            "Amenity": Amenity,
            "BaseModel": BaseModel,
            "City": City,
            "Place": Place,
            "Review": Review,
            "State": State,
            "User": User
        }

    # string - path to the JSON file
    __file_path = "./dev/file.json"
    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
        """
            returns the dictionary __objects
        """
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        """
            sets in __objects the obj with key <obj class name>.id
        """
        key = obj.__class__.__name__ + "." + obj.id
        self.__objects[key] = obj

    def save(self):
        """
            serializes __objects to the JSON file (path: __file_path)
        """
        json_objects = {}

        for key, value in self.__objects.items():
            json_objects[key] = value.to_json(saving_file_storage=True)
        with open(self.__file_path, mode='w', encoding='utf-8') as f:
            json.dump(json_objects, f)

    def reload(self):
        """
            deserializes the JSON file to __objects
        """
        try:
            with open(self.__file_path, mode='r', encoding='utf-8') as f:
                jo = json.load(f)
        except FileNotFoundError:
            return
        for ob_id, d in jo.items():
            cls_nm = jo[ob_id]["__class__"]
            self.__objects[ob_id] = classes[cls_nm](**jo[ob_id])

    def get(self, cls, id):
        """
            Retrieve an object using classname and id
        """
        if cls and id:
            fetch_obj = "{}.{}".format(cls, id)
            all_obj = self.all(cls)
            return all_obj.get(fetch_obj)
        return None

    def count(self, cls=None):
        """
            Return number of objects in filestorage
        """
        count = len(list(self.all(cls)))
        return count

    def delete(self, obj=None):
        """
            delete obj from __objects if it’s inside
        """
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def delete_all(self):
        """
            deletes all stored objects, for testing purposes
        """
        try:
            with open(FileStorage.__file_path, mode='w') as f_io:
                pass
        except FileNotFoundError:
            pass
        del FileStorage.__objects
        FileStorage.__objects = {}
        self.save()

    def close(self):
        """
            call reload() method for deserializing the JSON file to objects
        """
        self.reload()
