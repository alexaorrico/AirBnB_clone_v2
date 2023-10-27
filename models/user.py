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

        # When creating a new user or updating the password, hash the password
        if 'password' in kwargs:
            self.password = hashlib.md5(kwargs['password']
                                        .encode()).hexdigest()
        else:
            self.password = ""

    def to_dict(self, for_file_storage=False):
        # Create the dictionary to represent the object
        obj_dict = super().to_dict()

        # Remove the "password" key by default
        if not for_file_storage:
            obj_dict.pop('password', None)

        return obj_dict
