#!/usr/bin/python3
""" holds class User"""
from hashlib import md5
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models
from models.base_model import BaseModel, Base


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user", cascade="delete, all")
        reviews = relationship(
            "Review", backref="user", cascade="delete, all"
        )
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, __name, __value):
        """Encrypt user password"""
        if __name == "password":
            __value = md5(__value.encode()).hexdigest()
        return super().__setattr__(__name, __value)
