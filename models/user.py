#!/usr/bin/python3
""" holds class User"""
from models.base_model import BaseModel, Base
from os import getenv
import hashlib
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class User(BaseModel, Base):
    """Representation of a user """
    if getenv("HBNB_TYPE_STORAGE") == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
    else:
        email = ""
        password = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    @property
    def password(self):
        """Getter for the password attribute """
        return self.__password

    @password.setter
    def password(self, value):
        """Setter for the password attribute """
        self.__password = hashlib.md5(value.encode()).hexdigest()
