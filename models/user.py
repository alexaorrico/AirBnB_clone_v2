#!/usr/bin/python3
""" holds class User"""
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a user """
    __tablename__ = "users"
    if getenv("HBNB_TYPE_STORAGE", "fs") == "db":
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    @property
    def password(self):
        '''
            return hashed password
        '''
        return self._password

    @password.setter
    def password(self, value):
        '''
            fset the password with hash
        '''
        self._password = hashlib.md5(value.encode('utf8')).hexdigest()
