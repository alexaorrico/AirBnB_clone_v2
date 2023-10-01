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
        print("creating a new user")
        # super().__init__(*args, **kwargs)

        # hash user password if it's in kwargs
        if "password" in kwargs and kwargs["password"] is not None:
            # hash the password
            hashed_password = hashlib.md5(kwargs["password"].encode())\
                .hexdigest()
            kwargs["password"] = hashed_password

        self.password = kwargs.get('password', '')
        super().__init__(*args, **kwargs)
