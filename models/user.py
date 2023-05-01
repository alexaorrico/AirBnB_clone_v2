#!/usr/bin/python3
""" holds class User"""
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
from hashlib import md5
from os import getenv
import sqlalchemy
import models


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column((String(128)), nullable=False)
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
        if "password" in kwargs.keys():
            sh = md5(kwargs["password"].encode()).hexdigest()
            kwargs["password"] = sh
        super().__init__(*args, **kwargs)
