#!/usr/bin/python3
"""
user module
contains
The User Class inherits from BaseModel, Base
Since I am using my own setter/getter to encrypt the password
I need to redefine password as a protected class attribute, otherwise
the orm is lost and does not create the password column
"""
from models.base_model import BaseModel, Base, Table, Column, String
from sqlalchemy.orm import relationship, backref
import hashlib
from os import getenv
<<<<<<< HEAD


class User(BaseModel, Base):
    """
    User class
    """
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = "users"
=======
import sqlalchemy
from sqlalchemy import Column, String, Integer, Table
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a user """
    __tablename__ = 'users'
    if getenv("HBNB_TYPE_STORAGE") == "db":
>>>>>>> 0e125649dcfd402fd7b762fe147243315523b4f2
        email = Column(String(128), nullable=False)
        _password = Column("password", String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        reviews = relationship("Review", backref="user",
                               cascade="all, delete, delete-orphan")
        places = relationship("Place", backref="user",
                              cascade="all, delete, delete-orphan")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """
        initializes from BaseModel
        """
        value = kwargs.get("password", "")
#        kwargs["password"] = hashlib.md5(bytes(value.encode('utf-8')))
        super().__init__(*args, **kwargs)

    @property
    def password(self):
        return self.__dict__.get('_password', "")

    @password.setter
    def password(self, value):
        """
        hash the password

        Argument:
           value: password new value
        """
        b = bytes(value.encode("utf-8"))
        self.__dict__['_password'] = hashlib.md5(b).hexdigest()
