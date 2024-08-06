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
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """
        Retrieves an object based on the class and its ID.
        Args:
            cls (type): The class type of the object to retrieve.
            id (str): The ID of the object to retrieve.
        Returns:
            object: The object with the given class and ID,
            or None if not found.
        """
        # Check if the class is valid and the ID is a non-empty string
        if cls in classes.values() and id and type(id) == str:
            # Retrieve all objects of the given class
            d_obj = self.all(cls)
            # Iterate over each key-value pair in the dictionary
            for key, value in d_obj.items():
                # Check if the ID part of the key matches the given ID
                if key.split(".")[1] == id:
                    # Return the object if the ID matches
                    return value

        # Return None if no matching object is found
        return None

    def count(self, cls=None):
        """
        Counts the number of objects in storage matching the given class
        Args:
            cls (type, optional): The class type to count.
            If None, counts all objects.
        Returns:
            int: The number of objects found.
        """
        # Retrieve all objects, optionally filtering by class
        data = self.all(cls)
        # Check if the class is valid and filter data if necessary
        if cls in classes.values():
            data = self.all(cls)

        # Return the count of objects
        return len(data)
