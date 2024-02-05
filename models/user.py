#!/usr/bin/python3
""" holds class User"""
import hashlib
import os
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


def hash_password(string):
    """Hashing helper function"""
    md5 = hashlib.md5(bytes(string, encoding='utf-8'))
    return md5.hexdigest()


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
        if kwargs.get('password', False):
            kwargs['password'] = hash_password(kwargs["password"])
        super().__init__(*args, **kwargs)
