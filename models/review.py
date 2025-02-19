#!/usr/bin/python3
""" holds class Review"""
from os import getenv
import models
import sqlalchemy
from models.base_model import BaseModel, Base
from sqlalchemy import Column, ForeignKey, String


class Review(BaseModel, Base):
    """Representation of Review """
    if models.storage_t == 'db':
        __tablename__ = 'reviews'
        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        text = Column(String(1024), nullable=False)
    else:
        place_id = ""
        user_id = ""
        text = ""

    def __init__(self, *args, **kwargs):
        """initializes Review"""
        super().__init__(*args, **kwargs)

    def __str__(self):
        """Returns a string representation of the Review instance"""
        return "[Review] ({}) {}".format(self.id, self.__dict__)
