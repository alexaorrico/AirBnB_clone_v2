#!/usr/bin/python3
"""Defines the User class."""

import models
import hashlib
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class User(BaseModel, Base):
    """Representation of a user."""
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
        """Initializes a user object."""
        if kwargs:
            password = kwargs.pop('password', None)
            if password:
                # Hash the password using MD5
                hashed_password = hashlib.md5(password.encode("utf-8")).hexdigest()
                kwargs['password'] = hashed_password
        super().__init__(*args, **kwargs)
