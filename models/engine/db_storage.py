#!/usr/bin/python3
"""database storage engine"""

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import env
from models.amenity import Amenity
from models.base_model import Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {
    "User": User, "State": State, "City": City,
    "Amenity": Amenity, "Place": Place, "Review": Review
}


class DBStorage:
    """database storage engine for mysql storage"""
    __engine = None
    __session = None

    def __init__(self):
        """instantiate new dbstorage instance"""
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                env.HBNB_MYSQL_USER,
                env.HBNB_MYSQL_PWD,
                env.HBNB_MYSQL_HOST,
                env.HBNB_MYSQL_DB
            ), pool_pre_ping=True)

        if env.HBNB_ENV == 'test':
            self.drop_tables()

    def drop_tables(self):
        Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current db session all cls objects
        this method must return a dictionary: (like FileStorage)
        key = <class-name>.<object-id>
        value = object
        """
        dct = {}
        if cls is None:
            for c in classes.values():
                objs = self.__session.query(c).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    dct[key] = obj
                    del dct[key].__dict__['_sa_instance_state']
        else:
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = obj.__class__.__name__ + '.' + obj.id
                dct[key] = obj
                del dct[key].__dict__['_sa_instance_state']
        return dct

    def new(self, obj):
        """adds the obj to the current db session"""
        if obj is not None:
            try:
                self.__session.add(obj)
                self.__session.flush()
                self.__session.refresh(obj)
            except Exception as ex:
                self.__session.rollback()
                raise ex

    def get_session(self):
        """returns the current db session"""
        return self.__session

    def save(self):
        """commit all changes of the current db session"""
        self.__session.commit()

    def delete(self, obj=None):
        """ deletes from the current database session the obj
            is it's not None
        """
        if obj is not None:
            self.__session.query(obj.__class__)\
                .filter(
                    obj.__class__.id == obj.id).delete()

    def reload(self):
        """reloads the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(session_factory)()

    def close(self):
        """closes the working SQLAlchemy session"""
        self.__session.close()
