#!/usr/bin/python3
""" Database storage module """
import os
import importlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.amenity import Amenity
from models.base_model import Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

class DBStorage:
    """ Database storage class that will manage the database """
    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                       .format(os.getenv('HBNB_MYSQL_USER'),
                                               os.getenv('HBNB_MYSQL_PWD'),
                                               os.getenv('HBNB_MYSQL_HOST'),
                                               os.getenv('HBNB_MYSQL_DB')),
                                       pool_pre_ping=True)

        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query all objects in the database"""
        objects = {}
        if cls:
            query_result = self.__session.query(cls).all()
        else:
            classes = [State, City, User, Place, Review, Amenity]
            query_result = []
            for c in classes:
                query_result.extend(self.__session.query(c).all())

        for obj in query_result:
            key = '{}.{}'.format(type(obj).__name__, obj.id)
            objects[key] = obj

        return objects

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database"""
        Base.metadata.create_all(self.__engine)

        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = Session()

    def close(self):
        """close the current session"""
        self.__session.close()

    def get(self, cls, id):
        """retrieves one object"""
        key = '{}.{}'.format(cls.__name__, id)
        return self.all(cls).get(key)

    def count(self, cls=None):
        if cls:
            return len(self.all(cls))
        return len(self.all())