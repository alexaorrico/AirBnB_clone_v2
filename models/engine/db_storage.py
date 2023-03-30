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


classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class DBStorage:
    """
    This class is used to interact with the MySQL database.
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        Initializes a new DBStorage object.
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
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """
        Query on the current database session.
        """
        new_dict = {}
        if cls is None:
            for cls in classes.values():
                objs = self.__session.query(cls).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        else:
            objs = self.__session.query(classes[cls]).all()
            for obj in objs:
                key = obj.__class__.__name__ + '.' + obj.id
                new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """
        Add the object to the current database session.
        """
        self.__session.add(obj)

    def save(self):
        """
        Commit all changes of the current database session.
        """
        self.__session.commit()

    def get(self, cls, id):
        '''
            Retrieve one object
        '''
        obj = self.__session.query(eval(cls)).filter_by(id=id).first()
        return obj

    def count(self, cls=None):
        '''
           Count the number of objects in storage
        '''
        count = 0
        class_dict = self.all(cls)
        count = len(class_dict)
        return count

    def delete(self, obj=None):
        """
        Delete from the current database session obj if not None.
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Reloads data from the database.
        """
        Base.metadata.create_all(bind=self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session()

    def close(self):
        """
        Call remove() method on the private session attribute.
        """
        self.__session.close()