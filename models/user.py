#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import hashlib


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
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

    def __setattr__(self, name, value):
        """ it's documented, see? """
        if name == 'password':
            value = hashlib.md5(value.encode()).hexdigest()
        self.__dict__[name] = value
    '''
    @property
    def password(self):
        """ straight from the netherlands """
        return self.password

    @password.setter
    '''
    '''
    def password(self, password):
        """ this ones from china """
        m = hashlib.md5(password.encode()).hexdigest()
        return m
    '''
