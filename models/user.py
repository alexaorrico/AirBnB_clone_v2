#!/usr/bin/python3
"""Module that holds the User class"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from hashlib import md5


class User(BaseModel, Base):
    """Class representing a user model"""
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
        """Initializes user instance"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """Sets the password with md5 encryption"""
        if name == "password" and value is not None:
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)
