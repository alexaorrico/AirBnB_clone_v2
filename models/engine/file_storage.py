#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if not cls:
            return self.__objects
        else:
            new = {
                obj: key for obj, key in self.__objects.items()
                if type(key) == cls
            }
            return new

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """deletes obj from __objects if it's in there"""
        FileStorage.__objects = {
            key: value for key,
            value in FileStorage.__objects.items() if value != obj
        }

    def get(self, cls, id):
        """retrieve one object if exists"""
        dict = self.all(cls)
        for i, j in dict.items():
            obj = cls + '.' + id
            if i == obj:
                return(j)
        return(None)

    def count(self, cls=None):
        """count the num of objects in particular cls"""
        count = 0
        dict = self.all(cls)
        count = len(dict)
        return(count)

    def close(self):
        self.reload()
