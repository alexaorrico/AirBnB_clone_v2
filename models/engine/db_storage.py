#!/usr/bin/python3
"""
Database storage engine using SQLAlchemy with a mysql+mysqldb database
"""

import os
import models
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import re  # Added import for re

name2class = {
    'Amenity': Amenity,
    'City': City,
    'Place': Place,
    'State': State,
    'Review': Review,
    'User': User
}


class DBStorage:
    """
    Database Storage
    """

    __engine = None
    __session = None

    def __init__(self):
        """Initializes the object"""
        user = os.getenv('HBNB_MYSQL_USER')
        passwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        database = os.getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, passwd, host, database))
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """returns a dictionary of all the objects present"""
        if not self.__session:
            self.reload()
        objects = {}
        if isinstance(cls, str):
            cls = name2class.get(cls, None)
        if cls:
            for obj in self.__session.query(cls):
                objects[obj.__class__.__name__ + '.' + obj.id] = obj
        else:
            for cls in name2class.values():
                for obj in self.__session.query(cls):
                    objects[obj.__class__.__name__ + '.' + obj.id] = obj
        return objects

    def reload(self):
        """reloads objects from the database"""
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(session_factory)

    def new(self, obj):
        """creates a new object"""
        self.__session.add(obj)

    def save(self):
        """saves the current session"""
        self.__session.commit()

    def delete(self, obj=None):
        """deletes an object"""
        if not self.__session:
            self.reload()
        if obj:
            self.__session.delete(obj)

    def close(self):
        """Dispose of the current session if active"""
        self.__session.remove()

    def get(self, cls, id):
        """
        gets an object
        Args:
            cls (str): class name
            id (str): object ID
        Returns:
            an object based on class name and its ID
        """
        obj_dict = models.storage.all(cls)
        for k, v in obj_dict.items():
            matchstring = cls + '.' + id
            if k == matchstring:
                return v

        return None

    def count(self, cls=None):
        """
        counts number of objects of a class (if given)
        Args:
            cls (str): class name
        Returns:
            number of objects in class, if no class name given
            return total number of objects in database
        """
        obj_dict = models.storage.all(cls)
        return len(obj_dict)
