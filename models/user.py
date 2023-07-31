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
        __table_args__ = {"mysql_default_charset": "latin1"}
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
        """initializes user
        if User object is created or password updated,
        the password is hashed to a MD5 value
        """
        if "password" in kwargs:
            kwargs["password"] = hashlib.md5(
                kwargs["password"].encode()).hexdigest()
        super().__init__(*args, **kwargs)

    def save_passwd(self):
        """Hashing the password and the save it to db """
        if "password" in self.__dict__:
            self.password = hashlib.md5(self.password.encode()).hexdigest()
        super().save()
