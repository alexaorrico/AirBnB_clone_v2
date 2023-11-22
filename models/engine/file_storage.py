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
c_lasses = {Amenity: "Amenity", BaseModel: "BaseModel", City: "City",
         Place: "Place", Review: "Review", State: "State", User: "User"}


class FileStorage:
  """
  FileStorage serializes instances to a JSON file 
  and deserializes back to instances.
  """

  # string - path to the JSON file
  __file_path = "file.json"
  # dictionary - empty but will store all objects by <class name>.id
  __objects = {}

  def all(self, cls=None):
      """
      Returns the dictionary __objects.

      Args:
          cls (Class, optional): The class of the objects to return.

      Returns:
          dict: A dictionary of all objects of the given class.
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
      Sets in __objects the obj with key <obj class name>.id.

      Args:
          obj (Base): The object to add to __objects.
      """
      if obj is not None:
          key = obj.__class__.__name__ + "." + obj.id
          self.__objects[key] = obj

  def save(self):
      """
      Serializes __objects to the JSON file (path: __file_path).
      """
      json_objects = {}
      for key in self.__objects:
          json_objects[key] = self.__objects[key].to_dict()
      with open(self.__file_path, 'w') as f:
          json.dump(json_objects, f)

  def reload(self):
      """
      Deserializes the JSON file to __objects.
      """
      try:
          with open(self.__file_path, 'r') as f:
              jo = json.load(f)
          for key in jo:
              self.__objects[key] = classes[jo[key]["__class__"]](**jo[key])
      except:
          pass

  def delete(self, obj=None):
      """
      Delete obj from __objects if it’s inside.

      Args:
          obj (Base, optional): The object to delete from __objects.
      """
      if obj is not None:
          key = obj.__class__.__name__ + '.' + obj.id
          if key in self.__objects:
              del self.__objects[key]

  def close(self):
      """
      Call reload() method for deserializing 
      the JSON file to objects.
      """
      self.reload()

  def get(self, cls, id):
      """
      Get an object from __objects.

      Args:
          cls (Class): The class of the object to get.
          id (str): The ID of the object to get.

      Returns:
          Base: The object with the given class and ID.
      """
      key = c_lasses[cls] + '.' + id
      try:
          return self.__objects[key]
      except KeyError:
          return None

  def count(self, cls=None):
      """
      Count the number of objects of the given class in __objects.

      Args:
          cls (Class, optional): The class of the objects to count.

      Returns:
          int: The number of objects of the given class in __objects.
      """
      if cls is None:
          return len(self.__objects)
      else:
          count_list = []
          for item in self.__objects.values():
              if item.to_dict()['__class__'] == c_lasses[cls]:
                 count_list.append(item)
          return len(count_list)
