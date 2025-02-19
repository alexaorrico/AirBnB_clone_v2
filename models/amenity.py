#!/usr/bin/python
""" holds class Amenity"""
from os import getenv
import models
import sqlalchemy
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """Representation of Amenity """
    if models.storage_t == 'db':
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes Amenity"""
        super().__init__(*args, **kwargs)

    def __str__(self):
        """Returns a string representation of the Amenity instance"""
        return "[Amenity] ({}) {}".format(self.id, self.__dict__)
