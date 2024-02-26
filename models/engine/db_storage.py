#!/usr/bin/python3
"""
DBStorage
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
    """
    database
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        Instantiate
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
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        all
        """
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """
        new
        """
        self.__session.add(obj)

    def save(self):
        """
        save
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        delete
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """
        reload
        """
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def get(self, cls, id):
        """
        get
        """
        if type(cls) == str:
            cls = classes.get(cls)
        if cls is None:
            return None
        return self.__session.query(cls).filter(cls.id == id).first()

    def count(self, cls=None):
        """
        count
        """
        if type(cls) is str:
            cls = classes.get(cls)
        if cls is None:
            return len(self.all())
        return len(self.all(cls))

    def close(self):
        """
        close
        """
        self.__session.remove()
