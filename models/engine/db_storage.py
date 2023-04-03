#!/usr/bin/python3
""" Database storage module """
from sqlalchemy import create_engine
# import declarative base
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.state import State
from models.city import City
from models.user import User
from models.base_model import Base


class DBStorage:
    """ Database storage class that will manage the database.
    Returns:
        type: description
    """
    # private class attributes
    __engine = None
    __session = None

    def __init__(self):
        """ Intialize the database storage
        """
        # get environment variables
        user = os.getenv('HBNB_MYSQL_USER')
        passwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db = os.getenv('HBNB_MYSQL_DB')
        env = os.getenv('HBNB_ENV')

        db_path = ('mysql+mysqldb://{}:{}@{}/{}'
                   .format(user, passwd, host, db))

        self.__engine = create_engine(db_path, pool_pre_ping=True)
        # drop all tables if the environment variable HBNB_ENV is equal to test
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ query on the current database session """
        # create a dictionary
        obj_dict = {}
        if cls is None:
            classes = [State, City, User, Place, Review, Amenity]
            for class_name in classes:
                for obj in self.__session.query(class_name):
                    key = obj.__class__.__name__ + '.' + obj.id
                    obj_dict[key] = obj
        else:
            for obj in self.__session.query(cls):
                key = obj.__class__.__name__ + '.' + obj.id
                obj_dict[key] = obj
        return obj_dict

    def new(self, obj):
        """ add the object to the current database session """
        self.__session.add(obj)

    def save(self):
        """ commit all changes of the current database session """
        try:
            self.__session.commit()
        except Exception:
            self.__session.rollback()
        finally:
            self.__session.close()

    def delete(self, obj=None):
        """ delete from the current database session obj if not None """
        if obj is not None:
            self.__session.delete(obj)
            self.save()

    def reload(self):
        """ create all tables in the database """
        Base.metadata.create_all(self.__engine)
        # create a configured "Session" class
        sec = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sec)
        # create a Session
        self.__session = Session()

    def close(self):
        """ call close() method on the class Session
        """
        self.__session.close()

    def get(self, cls, id):
        """ Retrieves one object """
        if cls and id:
            key = cls.__name__ + '.' + id
            return self.all(cls).get(key)
        return None

    def count(self, cls=None):
        """ Counts the number of objects in storage """
        if cls:
            return len(self.all(cls))
        return len(self.all())
