#!/usr/bin/python3
""" holds class User"""
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
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user",
                              cascade="all, delete-orphan")
        reviews = relationship("Review", backref="user",
                               cascade="all, delete-orphan")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __setattr__(self, name, value):
        """ Sets the password as md5 hash """
        import hashlib
        if name == "password":
            # encode string value into bytes
            value = hashlib.md5(value.encode())
            # return encoded data in hexadecimal format
            value = value.hexdigest()
        super.__setattr__(self, name, value)

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
