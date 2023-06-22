#!/usr/bin/python3
"""Is module defines a class to manage file storage for hbnb clone."""
import json


class FileStorage:
    """Is class manages storage of hbnb models in JSON format."""

    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Return a dictionary or filtered list of models in storage."""
        if cls is None:
            return FileStorage.__objects
        filtered_objects = {}
        for key, value in FileStorage.__objects.items():
            class_name = key.split('.')[0]
            if class_name == cls.__name__:
                filtered_objects[key] = value
        return filtered_objects

    def new(self, obj):
        """Add a new object to the storage dictionary."""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Save the storage dictionary to a file."""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f, indent=2)

    def reload(self):
        """Load the storage dictionary from a file."""
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
        """Delete an object from the storage if it exists."""
        if obj is not None:
            key = f'{obj.__class__.__name__}.{obj.id}'
            if key in FileStorage.__objects:
                del FileStorage.__objects[key]

    def close(self):
        """Close the file storage and reload the data from JSON file."""
        self.reload()

    def get(self, cls, id):
        """Retrieve an object"""
        if cls is not None and type(cls) is str and id is not None and\
           type(id) is str and cls in classes:
            key = cls + '.' + id
            obj = self.__objects.get(key, None)
            return obj
        else:
            return None

    def count(self, cls=None):
        """Count number of objects in storage"""
        total = 0
        if type(cls) == str and cls in classes:
            total = len(self.all(cls))
        elif cls is None:
            total = len(self.__objects)
        return total
