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
        """ this querys the db session and returns
            a dict of all objects in the query """
        if not self.__session:
            return {}
        from models.user import User
        from models.city import City
        from models.place import Place
        from models.state import State
        from models.review import Review
        from models.amenity import Amenity
        name_to_class_mapper = {"User": User, "City": City, "Place": Place,
                                "State": State, "Review": Review,
                                "Amenity": Amenity}
        if not cls:
            cls_list = name_to_class_mapper.values()
            res_list = []
            res_dict = {}
            for entry in cls_list:
                res = self.__session.query(entry).all()
                res_list.extend(res)
            for entry in res_list:
                x = entry
                res_dict[f"{entry.to_dict()['__class__']}"
                         f".{entry.id}"] = x.__str__()
            return res_dict
        else:
            if type(cls) is not str:
                if cls.__name__ not in name_to_class_mapper:
                    return {}
                res = self.__session.query(name_to_class_mapper
                                           [cls.__name__]).all()
                res_dict = {}
                for entry in res:
                    res_dict[f"{cls}.{entry.id}"] = entry
            else:
                if cls not in name_to_class_mapper:
                    return {}
                res = self.__session.query(name_to_class_mapper
                                           [cls]).all()
                res_dict = {}
                for entry in res:
                    res_dict[f"{cls}.{entry.id}"] = entry
            return res_dict

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
        """Retrieves the specified object"""
        if cls:
            obj = self.__session.get(cls, id)
            return obj
        return None

    def count(self, cls=None):
        """Counts the number of objects in storage"""
        return len(self.all(cls))
