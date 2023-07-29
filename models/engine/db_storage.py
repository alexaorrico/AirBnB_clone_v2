#!/usr/bin/python3
"""
Contains the class DBStorage
"""

from models.amenity import Amenity
from models.base_model import Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
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
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if self.__session and \
                    (cls is None or cls is classes[clss] or cls is clss):
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        if self.__session:
            self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        if self.__session:
            self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if self.__session and obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        if self.__session:
            self.__session.remove()

    def get(self, cls, id):
        """Returns the object based on the class and its ID or None if  not
        found
        Args:
            cls: defines the table to find row in
            id: id of the row to return
        Return:
            None or object with `cls.id == id`
        """
        if self.__session and cls in classes.values() and id:
            return (self.__session.query(cls).filter(cls.id == id).one())
        return None

    def count(self, cls=None):
        """Counts the number of object in the storage matching the given class

        Args:
            cls (optional): defines the table to count it rows
        Returns:
            The number of object in storage matching the given class.
            if no class is passed, returns the count of all object in storage
            """
        if self.__session:
            row_count = 0
            if cls:
                row_count = self.__session.query(cls).count()
            else:
                for cls in classes.values():
                    row_count += self.__session.query(cls).count()
            return row_count
