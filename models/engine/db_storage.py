#!/usr/bin/python3
"""db_storage.py use database"""
import os

import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.review import Review
from models.place import Place
from models.amenity import Amenity
from models.state import State
from models.city import City


class DBStorage:
    """represents database storage"""
    __engine = None
    __session = None

    """
    set env variables depending on your OS
    """

    def __init__(self):
        """initialize object"""
        user = os.getenv('HBNB_MYSQL_USER')
        password = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        database = os.getenv('HBNB_MYSQL_DB')

        self.__engine = sqlalchemy.create_engine(
            'mysql+mysqldb://{}:{}@{}:3306/{}'
            .format(user,
                    password,
                    host,
                    database), pool_pre_ping=True)

        if os.getenv('HBNB_ENV') == "test":
            # from models.base_model import Base
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """gets all objects depending on the class name"""

        classes = {
            'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
        }
        obj_dict = {}
        if cls is not None and cls in classes:
            class_objects = self.__session.query(classes[cls]).all()
            for obj in class_objects:
                key = obj.__class__.__name__ + "." + obj.id
                obj_dict[key] = obj

        if cls is None:
            for cls in classes:
                class_objects = self.__session.query(classes[cls]).all()
                for obj in class_objects:
                    key = obj.__class__.__name__ + "." + obj.id
                    obj_dict[key] = obj

        return obj_dict

    def new(self, obj):
        """adds the object to the current session"""
        self.__session.add(obj)

    def save(self):
        """commits all changes of the current session"""
        self.__session.commit()

    def delete(self, obj=None):
        """deletes from the current session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        session = scoped_session(session_factory)
        self.__session = session()

    def close(self):
        """ destroying a session """
        self.__session.close()

    def get(self, cls, id):
        """ retrives one object and return it """
        if cls and id:
            key = "{}.{}".format(cls.__name__, id)
            the_objects = self.all(cls)
            return the_objects.get(key)
        return None

    def count(self, cls=None):
        """ count number of objects in storage """
        return len(self.all(cls))
