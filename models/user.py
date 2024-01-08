#!/usr/bin/python3
""" holds class User"""
from hashlib import md5 as hashit
from models.base_model import BaseModel, Base
from os import getenv
import models
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
        """initializes user"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, key, value):
        """sets hashed password instead of plain text"""
        if key == "password":
            value = hashit(value.encode()).hexdigest()
        super().__setattr__(key, value)
