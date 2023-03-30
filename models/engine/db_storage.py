#!/usr/bin/python3

"""
Contains the DBStorage class which interacts with a MySQL database.
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

# Dictionary of all available classes and their corresponding models
CLASS_MODELS = {"Amenity": Amenity, "City": City, "Place": Place,
                "Review": Review, "State": State, "User": User}


class DBStorage:
    """
    Represents a database storage engine
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        Instantiate a DBStorage object with a connection to a MySQL database
        """
        MYSQL_USER = getenv('HBNB_MYSQL_USER')
        MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        MYSQL_DB = getenv('HBNB_MYSQL_DB')
        ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(MYSQL_USER, MYSQL_PWD,
                                             MYSQL_HOST, MYSQL_DB))
        if ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Retrieve a dictionary of all objects in the current session
        """
        obj_dict = {}
        for cls_name, cls_model in CLASS_MODELS.items():
            if cls is None or cls is cls_model or cls is cls_name:
                objs = self.__session.query(cls_model).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    obj_dict[key] = obj
        return obj_dict

    def new(self, obj):
        """
        Add an object to the current session
        """
        self.__session.add(obj)

    def save(self):
        """
        Commit all changes made to the current session
        """
        self.__session.commit()

    def get(self, cls, id):
        """
        Retrieve a single object based on class name and object id
        """
        obj = self.__session.query(eval(cls)).filter_by(id=id).first()
        return obj

    def count(self, cls=None):
        """
        Count the number of objects in the current session
        """
        count = 0
        obj_dict = self.all(cls)
        count = len(obj_dict)
        return count

    def delete(self, obj=None):
        """
        Remove an object from the current session
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """
        Reload data from the database
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session

    def close(self):
        """
        Close the current session
        """
        self.__session.remove()
