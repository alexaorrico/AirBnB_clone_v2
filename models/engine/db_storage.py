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


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
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
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """
        This method creates tables and a new database session
        """
        try:
            # Clear the existing session, if any
            if self.__session:
                self.__session.close()

            # Create tables
            Base.metadata.create_all(self.__engine)

            # Use existing scoped session class &assign a new session to it
            self.__session = scoped_session(
                    sessionmaker(bind=self.__engine, expire_on_commit=False))
        except Exception as e:
            print(f"Error during reload: {e}")
            raise  # Reraise the exception to see the full traceback

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    # Retrieves an obj from the DB based on the class name & obj ID.

    def get(self, cls, id):
        """
        Retrieves an obj from the db based on
        the class name (cls) and obj ID (id)
        """
        if cls in classes.values() and id and type(id) == str:
            d_obj = self.all(cls)
            for key, value in d_obj.items():
                if key.split(".")[1] == id:
                    return value
                return None

    # Counts the number of objects in storage

    def count(self, cls=None):
        """
        This method counts the nbr of obj in storage matching the given class.
        """
        obj_data = self.all(cls)
        if cls in classes.values():
            obj_data = self.all(cls)
            return len(obj_data)
