#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.city import City
from models.state import State
from models.user import User
from models.place import Place
from models.review import Review


class DBStorage:
    """The class DBStorage is defined for database storage in Python."""

    __engine = None
    __session = None

    def __init__(self):
        """Is the constructor method for a Python class."""
        user = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        database = getenv('HBNB_MYSQL_DB')
        env = getenv('HBNB_ENV')

        self.__engine = create_engine(
            f'mysql+mysqldb://{user}:{password}@{host}/{database}',
            pool_pre_ping=True,
            )
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Is a method definition in a Python class that takes an optional\
        argument 'cls'."""
        session = self.__session
        classes = [User, State, City, Amenity, Place, Review]

        if cls:
            query = session.query(cls).all()
        else:
            query = []
            for cls in classes:
                query += session.query(cls).all()

        objects = {}
        for obj in query:
            key = f"{type(obj).__name__}.{obj.id}"
            objects[key] = obj

        return objects

    def new(self, obj):
        """Is function "new" takes in an object as a parameter."""
        self.__session.add(obj)

    def save(self):
        """Is function "save" is defined, but its implementation\
        is not shown."""
        self.__session.commit()

    def delete(self, obj=None):
        """Is function deletes an object from a session in Python."""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Is function "reload" is not defined and therefore cannot be\
        summarized."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def get(self, cls, id):
        """Is retrieve an object based on the class and its ID."""
        key = f"{cls.__name__}.{id}"
        return self.__session.query(cls).filter_by(id=id).first()

    def count(self, cls=None):
        """Count the number of objects in storage matching the given class."""
        if cls:
            return self.__session.query(cls).count()
        else:
            return self.__session.query(State).count()

    def close(self):
        """Close the database storage session."""
        if self.__session is not None:
            self.__session.close()
