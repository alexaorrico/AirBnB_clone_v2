#!/usr/bin/python3
"""Defines the User class."""
import models
import hashlib
import sqlalchemy
from os import getenv
from models.base_model import BaseModel, Base
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
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """Initializes a User."""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """Encodes passwords using MD5 before setting an attribute."""
        if name == "password":
            value = value.encode("utf-8")
            value = hashlib.md5(value).hexdigest()
        object.__setattr__(self, name, value)
