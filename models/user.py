#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from hashlib import md5


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

    """
    Security is VERY important and storing passwords in plain text is
    a horible idea.  This update incorporates md5, which isn't perfect
    but it's better than nothing
    """
    def __setattr__(self, key, value):
        """set encrypted password for users"""
        if key == 'password':
            value = md5(value.encode()).hexdigest()
        super().__setattr__(key, value)

    def to_dict(self, save_to_disk=True):
        """ returns a dictionary containning all keys/values of the instance"""
        new_dict = super().to_dict()
        if not save_to_disk and 'password' in new_dict:
            del new_dict['password']
        return new_dict
