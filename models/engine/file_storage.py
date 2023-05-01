#!/usr/bin/python3
""" Defines FileStorage class. """
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """
    Serializes instances to a JSON file and deserializes
    JSON file to instances.
    Attributes:
        __file_path (str): Path to the JSON file.
        __objects (dict): Store all objects.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """ Returns the dictionary __objects. """
        if cls is not None:
            if type(cls) == str:
                cls = eval(cls)
            cls_dict = {}
            for key, value in self.__objects.items():
                if type(value) == cls:
                    cls_dict[key] = value
            return cls_dict

        return self.__objects

    def new(self, obj):
        """ Sets in __objects the obj with key<obj class name>.id."""
        self.__objects["{}.{}".format(type(obj).__name__, obj.id)] = obj

    def save(self):
        """ Serializes __objects to the JSON file."""
        odict = {o: self.__objects[o].to_dict() for o in self.__objects.keys()}
        with open(self.__file_path, "w", encoding="utf-8") as myfile:
            json.dump(odict, myfile)

    def reload(self):
        """Deserialize the JSON file __file_path to __objects, if it exists."""
        try:
            with open(self.__file_path, "r", encoding="utf-8") as myfile:
                for o in json.load(myfile).values():
                    name = o["__class__"]
                    del o["__class__"]
                    self.new(eval(name)(**o))
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Delete obj from __objects if it’s inside - if obj is equal to None,
        The method should not do anything
        """
        try:
            del self.__objects["{}.{}".format(type(obj).__name__, obj.id)]
        except (AttributeError, KeyError):
            pass

    def close(self):
        """Call the reload method."""
        self.reload()

    def get(self, cls, id):
        """
            retrieves one object based on class name and id
        """
        if cls and id:
            fetch_obj = "{}.{}".format(cls, id)
            all_obj = self.all(cls)
            return all_obj.get(fetch_obj)
        return None

    def count(self, cls=None):
        """
        count of all objects in storage
        """
        return (len(self.all(cls)))
