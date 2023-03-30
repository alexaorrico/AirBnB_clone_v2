#!/usr/bin/python3

"""
Contains the DBStorage class
"""

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class DBStorage:
    """
    Database Storage
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        Initializes a new instance of the DBStorage class
        """
        user = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        database = getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(user, password, host, database),
                                      pool_pre_ping=True)

        if getenv('HBNB_ENV') == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Returns a dictionary of all objects of a given class or all objects
        in the database
        """
        new_dict = {}
        classes = [Amenity, City, Place, Review, State, User]

        if cls is None:
            for cls in classes:
                for obj in self.__session.query(cls):
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    new_dict[key] = obj
        else:
            if cls in classes:
                for obj in self.__session.query(cls):
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """
        Adds the object to the current database session
        """
        self.__session.add(obj)

    def save(self):
        """
        Commits all changes to the database
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Deletes an object from the database
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Creates all tables in the database and starts a new session
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """
        Closes the current session
        """
        self.__session.close()
