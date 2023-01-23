#!/usr/bin/python3
""" holds class User"""
import hashlib

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

    def __setattr__(self, __name: str, __value):
        """Override set attribute to hijack and hash the password setting"""
        if __name == "password":
            __value = hashlib.md5(__value.encode()).hexdigest()
        return super().__setattr__(__name, __value)

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
