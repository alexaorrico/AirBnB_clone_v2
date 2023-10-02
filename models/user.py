#!/usr/bin/python3
""" holds class User"""
import models
import hashlib as hlib
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
        """
            initializes user
        """
        if (kwargs):
            # get password from dict
            passwd = kwargs.pop('password', None)
            if (passwd):
                # create a hash object (MD5)
                hsh = hlib.md5()

                # add password to hash object
                hsh.update(passwd.encode('utf-8'))

                # get the hex value of password
                hsh_pswd = hsh.hexdigest()

                # set hashed password to dictionary
                kwargs['password'] = hsh_pswd

        super().__init__(*args, **kwargs)
