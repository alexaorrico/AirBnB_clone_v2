#!/usr/bin/python3
""" holds class User"""
import hashlib
import models
from models.base_model import BaseModel, Base
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
        """initializes user"""
        super().__init__(*args, **kwargs)

        # Hash the password if present in the arguments
        if 'password' in kwargs:
            self.set_password(kwargs['password'])

    def set_password(self, password):
        """Hashes the password using MD5"""
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        self.password = hashed_password

    def to_dict(self, include_password=False):
        """Converts the User instance to a dictionary"""
        data = super().to_dict()
        if include_password:
            data['password'] = self.password
        return data
