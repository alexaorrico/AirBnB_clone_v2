#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
import hashlib
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
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user and hash user password"""
        password = kwargs.get('password')
        hashed = hashlib.new('md5')
        hashed.update(bytes("{}".format(password), encoding='utf-8'))
        if kwargs.get("password"):
            kwargs['password'] = hashed.hexdigest()
        super().__init__(*args, **kwargs)
