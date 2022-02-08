#!/usr/bin/python3
""" holds class User"""
import hashlib
from os import getenv

import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

import models
from models.base_model import Base, BaseModel


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

    def __setattr__(self, __name: str, __value):
        """Overrides the __setattr__ method"""
        if __name == "password":
            md5_hash = hashlib.md5(bytes(__value, "utf-8"))
            object.__setattr__(self, __name, md5_hash.hexdigest())
        else:
            object.__setattr__(self, __name, __value)
