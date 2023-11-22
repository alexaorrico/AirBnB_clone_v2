#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"Amenity": Amenity, "City": City,
         "Place": Place, "Review": Review, "State": State, "User": User}
c_lasses = {Amenity: "Amenity", BaseModel: "BaseModel", City: "City",
         Place: "Place", Review: "Review", State: "State", User: "User"}


class DBStorage:
  """
  DBStorage interacts with the MySQL database and provides methods for querying, adding, saving, and deleting objects.
  """
  __engine = None
  __session = None

  def __init__(self):
      """
      Instantiate a DBStorage object and set up the connection to the MySQL database.
      """
      HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
      HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
      HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
      HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
      HBNB_ENV = getenv('HBNB_ENV')
      self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                format(HBNB_MYSQL_USER,
                                       HBNB_MYSQL_PWD,
                                       HBNB_MYSQL_HOST,
                                       HBNB_MYSQL_DB))
      if HBNB_ENV == "test":
          Base.metadata.drop_all(self.__engine)

  def all(self, cls=None):
      """
      Query on the current database session and return a dictionary of all objects of the given class.

      Args:
          cls (Class, optional): The class of the objects to query.

      Returns:
          dict: A dictionary of all objects of the given class.
      """
      new_dict = {}
      for clss in classes:
          if cls is None or cls is classes[clss] or cls is clss:
              objs = self.__session.query(classes[clss]).all()
              for obj in objs:
                key = obj.__class__.__name__ + '.' + obj.id
                new_dict[key] = obj
      return (new_dict)

  def new(self, obj):
      """
      Add the object to the current database session.

      Args:
          obj (Base): The object to add to the session.
      """
      self.__session.add(obj)

  def save(self):
      """
      Commit all changes of the current database session.
      """
      self.__session.commit()

  def delete(self, obj=None):
      """
      Delete from the current database session obj if not None.

      Args:
          obj (Base, optional): The object to delete from the session.
      """
      if obj is not None:
          self.__session.delete(obj)

  def reload(self):
      """
      Reloads data from the database.
      """
      Base.metadata.create_all(self.__engine)
      sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
      Session = scoped_session(sess_factory)
      self.__session = Session

  def close(self):
      """
      Call remove() method on the private session attribute.
      """
      self.__session.remove()

  def get(self, cls, id):
      """
      Get an object from the database.

      Args:
          cls (Class): The class of the object to get.
          id (str): The ID of the object to get.

      Returns:
          Base: The object with the given class and ID.
      """
      key = c_lasses[cls] + '.' + id
      diction = self.all()
      if key in diction:
          return diction[key]

  def count(self, cls=None):
      """
      Count the number of objects of the given class in the database.

      Args:
          cls (Class, optional): The class of the objects to count.

      Returns:
          int: The number of objects of the given class in the database.
      """
      new_dict = {}
      for clss in classes:
          if cls is None or cls is classes[clss] or cls is clss:
              objs = self.__session.query(classes[clss]).all()
              for obj in objs:
                key = obj.__class__.__name__ + '.' + obj.id
                new_dict[key] = obj
      return len(new_dict)
