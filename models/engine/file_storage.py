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


class FileStorage:
    """serializes instances to a JSON file & deserializes back to instances"""
<<<<<<< HEAD
=======
    
>>>>>>> refs/remotes/origin/storage_get_count
    classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}

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
                self.__objects[key] = self.classes[jo[key]["__class__"]](**jo[key])
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

    def get(self, cls, id):
<<<<<<< HEAD
        """one object to be retrieved"""
        obj_dict = {}
        obj = None
        if cls:
            obj_dict = FileStorage.__objects.values()
            for item in obj_dict:
                if item.id == id:
                    obj = item
            return obj

    def count(self, cls=None):
        """number of objects in a storage to be counted"""
        if cls:
            obj_list = []
            obj_dict = FileStorage.__objects.values()
            for item in obj_dict:
                if type(item).__name__ == cls:
                    obj_list.append(item)
            return len(obj_list)
        else:
            obj_list = []
            for class_name in self.classes:
                if class_name == 'BaseModel':
                    continue
                obj_class = FileStorage.__objects
                for item in obj_class:
                    obj_list.append(item)
            return len(obj_list)
=======
        """ one object to be retrieved"""
        dict_obj = {}
        obj = None
        if cls:
            dict_obj = FileStorage.__objects.values()
            for a in dict_obj:
                if a.id == id:
                    obj = a
            return obj

    def count(self, cls=None):
        """ a number of objects in a class of a storage to be counted """
        if cls:
            objof_list = []
            objof_dict = FileStorage.__objects.values()
            for a in objof_dict:
                if type(a).__name__ == cls:
                    objof_list.append(a)
            return len(objof_list)
        else:
            objof_list = []
            for a in self.classes:
                if a == 'BaseModel':
                    continue
                objof_class = FileStorage.__objects
                for b in objof_class:
                    objof_list.append(b)
            return len(objof_list)
>>>>>>> refs/remotes/origin/storage_get_count
