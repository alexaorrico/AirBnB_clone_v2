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
        _password = Column("password", String(128), nullable=False)
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
        if kwargs.get("password", None):
                pwd = hashlib.md5(kwargs["password"].encode('utf-8'))
                kwargs["password"] = pwd.hexdigest()
        super().__init__(*args, **kwargs)

    @property
    def password(self):
        """getter for hashed password"""
        return self._password

    @password.setter
    def password(self, pwd):
        """setter for hashed password"""
        self._password = hashlib.md5(pwd.encode('utf-8')).hexdigest()
