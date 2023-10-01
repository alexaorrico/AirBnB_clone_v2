#!/usr/bin/python3
""" holds class User"""
import models
import hashlib
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

        if 'password' in kwargs:
            self.hash_password(kwargs['password'])

    def hash_password(self, password):
        '''
            Hash the user's password using SHA-256.
        '''
        salt = uuid.uuid4().hex  # Generate a random salt
        hashed_password = hashlib.sha256((salt + password).encode()).hexdigest()
        self.password = salt + ':' + hashed_password  # Store salt:hashed_password

    def is_valid_password(self, password):
        '''
            Check if a given password is valid for the user.
        '''
        if ':' not in self.password:
            # Password is not hashed properly
            return False

        salt, hashed_password = self.password.split(':')
        return hashed_password == hashlib.sha256((salt + password).encode()).hexdigest()
