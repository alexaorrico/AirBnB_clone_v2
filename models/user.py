#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import hashlib


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

    def set_password(self, password):
        """hash password"""
        is_hashed = True
        if len(password) != 32:
            is_hashed = False
        else:
            # if not all(c in "0123456789abcdef" for c in password):
            #     is_hashed = False
            for c in password:
                if c not in "0123456789abcdef":
                    is_hashed = False
                    break

        if is_hashed:
            super().__setattr__("password", password)
        else:
            password_b = password.encode("utf-8")
            hash_obj = hashlib.md5()
            hash_obj.update(password_b)
            pass_hashed = hash_obj.hexdigest()
            setattr(self, "password", pass_hashed)

    def __setattr__(self, key, value):
        """set User attributes"""
        if key == "password":
            self.set_password(value)
        else:
            super().__setattr__(key, value)
