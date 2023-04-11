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


class DBStorage:
    """interaacts with the MySQL database"""
    tables = {"Amenity": Amenity, "City": City,
              "Place": Place, "Review": Review, "State": State, "User": User}

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
        """Returns all data"""
        new_dict = {}
        if cls is not None:
            # name = DBStorage.tables[cls]
            all_obj = self.__session.query(cls).all()
            for obj in all_obj:
                index = obj.to_dict()['__class__'] + '.' + obj.id
                new_dict[index] = obj
        else:
            for elem in DBStorage.tables.values():
                all_obj = self.__session.query(elem).all()
                for obj in all_obj:
                    index = obj.to_dict()['__class__'] + '.' + obj.id
                    new_dict[index] = obj
        return new_dict

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
        """Method used to get object if is already in storage"""
        key_name = cls.__name__ + '.' + id
        for key, val in self.all().items():
            if key_name == key:
                return val
        return None

    def count(self, cls=None):
        """Method returning the number of instances of an obj"""
        return len(self.all(cls))
