#!/usr/bin/python3
'''
    Implementation of the User class which inherits from BaseModel
'''
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
import hashlib

class User(BaseModel, Base):
    '''
        Definition of the User class
    '''
    __tablename__ = "users"

    if getenv("HBNB_TYPE_STORAGE", "fs") == "db":
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user",
                              cascade="all, delete, delete-orphan")
        reviews = relationship("Review", backref="user",
                               cascade="all, delete, delete-orphan")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        if kwargs:
            encrypt = kwargs.pop('password', None)
            User.set_password(self, encrypt)
        super().__init__(*args, **kwargs)

    def set_password(self, _password):
        encrypt = hashlib.md5()
        encrypt.update(_password.encode("utf-8"))
        encrypt = encrypt.hexdigest()
        setattr(self, "password", encrypt)
