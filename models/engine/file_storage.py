#!/usr/bin/python3
'''
    Define class FileStorage
'''
import json
import models


class FileStorage:
    '''
        Serializes instances to JSON file and deserializes to JSON file.
    '''
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        '''
            Return the dictionary
        '''
        new_dict = {}
        if cls is None:
            return self.__objects

        if cls is not None:
            for k, v in self.__objects.items():
                if cls == k.split(".")[0]:
                    new_dict[k] = v
            return new_dict
        else:
            return self.__objects

    def get(self, cls, id):
        '''
            Retrieves one object if exists
        '''
        cls_dict = self.all(cls)
        for k, v in cls_dict.items():
            obj = cls + '.' + id
            if k == obj:
                return(v)
        return(None)

    def count(self, cls=None):
        '''
           counts the num of objects in particular cls
        '''
        count = 0
        cls_dict = self.all(cls)
        count = len(cls_dict)
        return(count)

    def new(self, obj):
        '''
            Set in __objects the obj with key <obj class name>.id
            Aguments:
                obj : An instance object.
        '''
        key = str(obj.__class__.__name__) + "." + str(obj.id)
        value_dict = obj
        FileStorage.__objects[key] = value_dict

    def save(self):
        '''
            Serializes __objects attribute to JSON file.
        '''
        objects_dict = {}
        for key, val in FileStorage.__objects.items():
            objects_dict[key] = val.to_dict()

        with open(FileStorage.__file_path, mode='w', encoding="UTF8") as fd:
            json.dump(objects_dict, fd)

    def reload(self):
        '''
            Deserializes the JSON file to __objects.
        '''
        try:
            with open(FileStorage.__file_path, encoding="UTF8") as fd:
                FileStorage.__objects = json.load(fd)
            for key, val in FileStorage.__objects.items():
                class_name = val["__class__"]
                class_name = models.classes[class_name]
                FileStorage.__objects[key] = class_name(**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        '''
        Deletes an obj
        '''
        if obj is not None:
            key = str(obj.__class__.__name__) + "." + str(obj.id)
            FileStorage.__objects.pop(key, None)
            self.save()

    def close(self):
        '''
        Deserialize JSON file to objects
        '''
        self.reload()

    def get(self, cls, id):
        """
        Retrieve one object
        @cls: class name
        @id: string representing the object ID
        Return: Object based on the class name and its ID, or None if not found
        """
        obj = self.__session.query(cls).get(id)
        if obj is None:
            return None
        return obj

    def count(self, cls=None):
        """
        Count the number of objects in storage:
        @cls: class name
        Return:
        """
        objs = self.all(cls)
        return (len(objs))
