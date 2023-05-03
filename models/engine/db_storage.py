#!/usr/bin/python3
from models.amenity import Amenity
from models.base_model import Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
import os
from os import getenv
from sqlalchemy import (create_engine, func)
from sqlalchemy.orm import (sessionmaker, scoped_session)
"""
This is the db_storage module.
This module deals with storing and retrieving data from a mysql database.
This module contains one class DBStorage.
"""


class DBStorage:
<<<<<<< HEAD
    """
    class DBStorage
    Save and retrieve data from a MySQL database using sqlAlchemy ORM

    **class attributes**
       __engine: private, sqlAlchemy engine
       __session: private, MySQL session

    instance attributes:
       __models_available: private, dictionary of <string> <class>
    """
=======

    classes = {"User": User, "BaseModel": BaseModel,
               "Place": Place, "State": State,
               "City": City, "Amenity": Amenity,
               "Review": Review}

    """interacts with the MySQL database"""
>>>>>>> 0e125649dcfd402fd7b762fe147243315523b4f2
    __engine = None
    __session = None

    def __init__(self):
<<<<<<< HEAD
        """
        initializes engine
        """
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            getenv('HBNB_MYSQL_USER'),
            getenv('HBNB_MYSQL_PWD'),
            getenv('HBNB_MYSQL_HOST'),
            getenv('HBNB_MYSQL_DB')))
        # adding, echo=True) shows SQL statements
        self.__models_available = {"User": User,
                                   "Amenity": Amenity, "City": City,
                                   "Place": Place, "Review": Review,
                                   "State": State}
        if getenv('HBNB_MYSQL_ENV', 'not') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        returns a dictionary of all the class objects
        """
        orm_objects = {}
        if cls:
            if cls in self.__models_available:
                for k in self.__session.query(
                        self.__models_available.get(cls)):
                    orm_objects[k.__dict__['id']] = k
        else:
            for i in self.__models_available.values():
                j = self.__session.query(i).all()
                if j:
                    for k in j:
                        orm_objects[k.__dict__['id']] = k
        return orm_objects
=======
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
                                             HBNB_MYSQL_DB),
                                      pool_pre_ping=True)
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        if cls:
            class_name = cls.__name__
            objs = self.__session.query(cls).all()
        else:
            objs = []
            for cls_name in self.classes:
                if cls_name == 'BaseModel':
                    continue
                cls = self.classes[cls_name]
                objs += self.__session.query(cls).all()
        return {obj.__class__.__name__ + '.' + obj.id: obj for obj in objs}
>>>>>>> 0e125649dcfd402fd7b762fe147243315523b4f2

    def new(self, obj):
        """
        adds a new obj to the session
        """
        self.__session.add(obj)

    def save(self):
        """
        saves the objects fom the current session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        deletes an object from the current session
        """
        if obj is not None:
            self.__session.delete(obj)
            self.__session.commit()

    def reload(self):
        """
        WARNING!!!! I'm not sure if Base.metadata.create_all needs to
        be in the init method
        """
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                                     expire_on_commit=False))

    def close(self):
        """
        close a session
        """
        self.__session.remove()

<<<<<<< HEAD
    def get(self, cls, id_):
        """
        Retrieve one object

        Arguments:
            cls: string representing a class name
            id_: string representing the object id, primary key

        Return:
           object of cls and id passed in argument or None
        """
        if (cls not in self.__models_available) or (id_ is None):
            return None
        return self.__session.query(
                self.__models_available[cls]).get(id_)

    def count(self, cls=None):
        """
        Number of objects in a certain class

        Arguments:
            cls: optional, string representing a class name (default None)

        Return:
            number of objects in that class or in total
            -1 if the argument is not valid
        """
        if cls is None:
            total = 0
            for v in self.__models_available.values():
                total += self.__session.query(v).count()
            return total
        if cls in self.__models_available.keys():
            return self.__session.query(self.__models_available[cls]).count()
        return -1
=======
    def get(self, cls, id):
        """ Retrieves an object from the database based on its class and ID"""
        if cls and id:
            return self.__session.query(cls).get(id)
        else:
            return None

    def count(self, cls=None):
        """Counts the number of objects in storage"""
        if cls:
            class_name = cls.__name__
            return self.__session.query(eval(class_name)).count()
        else:
            count = 0
            for cls_name in self.classes:
                if cls_name == 'BaseModel':
                    continue
                count += self.__session.query(eval(cls_name)).count()
            return count
>>>>>>> 0e125649dcfd402fd7b762fe147243315523b4f2
