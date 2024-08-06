#!/usr/bin/python3
"""
Define class FileStorage
"""
import json
import models


class FileStorage:
    """
    Serializes instances to a JSON file, deserializes JSON file to instances.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """
        Returns the dictionary of objects filtered by class type if provided.
        """
        if cls is None:
            return self.__objects
        new_dict = {}
        for k, v in self.__objects.items():
            if isinstance(v, cls):
                new_dict[k] = v
        return new_dict

    def new(self, obj):
        """
        Adds a new object to the storage dictionary.
        """
        key = f'{obj.__class__.__name__}.{obj.id}'
        self.__objects[key] = obj

    def save(self):
        """
        Serializes the __objects to the JSON file specified by __file_path.
        """
        obj_dict = {k: v.to_dict() for k, v in self.__objects.items()}
        with open(self.__file_path, 'w', encoding='utf-8') as f:
            json.dump(obj_dict, f)

    def reload(self):
        """
        Deserializes the JSON file to __objects.
        """
        try:
            with open(self.__file_path, 'r', encoding='utf-8') as f:
                objects = json.load(f)
            for k, v in objects.items():
                cls_name = v['__class__']
                cls = models.classes[cls_name]
                self.__objects[k] = cls(**v)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        Deletes obj from __objects if it’s inside.
        Args:
            obj (object): The object to delete.
        """
        if obj:
            key = f'{obj.__class__.__name__}.{obj.id}'
            if key in self.__objects:
                del self.__objects[key]
                self.save()

    def close(self):
        """
        Call reload() method for deserializing the JSON file to objects.
        """
        self.reload()

    def get(self, cls, id):
        """
        Retrieve one object based on the class name and its ID.
        """
        key = f'{cls.__name__}.{id}'
        return self.__objects.get(key, None)

    def count(self, cls=None):
        """
        Count the number of objects in storage.
        """
        if cls:
            return len(self.all(cls))
        return len(self.__objects)
