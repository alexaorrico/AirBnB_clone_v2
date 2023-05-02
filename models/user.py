#!/usr/bin/python3
""" holds class User"""
import hashlib
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        _password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        _password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
        if kwargs:
            if len(kwargs['password']) != 32:
                self._password = hashlib.md5(
                     kwargs['password'].encode('utf8')).hexdigest()
            else:
                self._password = kwargs['password']

    @property
    def password(self):
        """ getter to return hashed password """
        return self._password

    @password.setter
    def password(self, value):
        """ hashes the password """
        self._password = hashlib.md5(value.encode('utf8')).hexdigest()
