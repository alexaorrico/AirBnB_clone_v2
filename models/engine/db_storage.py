#!/usr/bin/python3
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from models.base_model import BaseModel, Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
import os

classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class DBStorage:
    """database storage class definition"""
    __engine = None
    __session = None

    def __init__(self):
        """initialization"""
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".format(
            os.getenv("HBNB_MYSQL_USER"), os.getenv("HBNB_MYSQL_PWD"),
            os.getenv("HBNB_MYSQL_HOST"), os.getenv("HBNB_MYSQL_DB")),
            pool_pre_ping=True)
        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """return dictionary of all objects"""
        allobjs = {}
        if cls:
            allobjs = {obj.__class__.__name__ + "." + obj.id: obj for
                       obj in self.__session.query(classes[cls]).all()}
        else:
            for tbl in Base.__subclasses__():
                table = self.__session.query(tbl).all()
                for obj in table:
                    allobjs[obj.__class__.__name__ + "." + obj.id] = obj
        return allobjs

    def new(self, obj):
        """add new object"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """save new object"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete object"""
        self.__session.delete(obj)

    def reload(self):
        """load all objects and create new session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def get(self, cls, id):
        """retrieve one object if exists"""
        dict = self.all(cls)
        for i, j in dict.items():
            obj = cls + '.' + id
            if i == obj:
                return(j)
        return(None)

    def count(self, cls=None):
        """count the num of objects in particular cls"""
        count = 0
        dict = self.all(cls)
        count = len(dict)
        return(count)

    def close(self):
        self.__session.close()
