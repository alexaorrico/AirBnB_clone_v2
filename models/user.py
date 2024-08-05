#!/usr/bin/python3
""" holds class User"""
import hashlib
import models
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String


class User(BaseModel, Base):
    """Representation of a user """
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        _password = Column('password', String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user", cascade="all, delete-orphan")  # noqa
        reviews = relationship("Review", backref="user", cascade="all, delete-orphan")  # noqa
    else:
        email = ""
        _password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """Initializes user"""
        super().__init__(*args, **kwargs)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, pwd):
        """Hashes password values"""
        self._password = hashlib.md5(pwd.encode()).hexdigest()

    def to_dict(self, save_to_disk=False):
        """Returns a dictionary representation of the User instance"""
        user_dict = super().to_dict(save_to_disk)
        if not save_to_disk:
            user_dict.pop('password', None)
        return user_dict
