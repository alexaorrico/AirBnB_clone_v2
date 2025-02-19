#!/usr/bin/python
""" holds class City"""
from os import getenv
import models
import sqlalchemy
from models.base_model import BaseModel, Base
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """Representation of city """
    __tablename__ = 'cities'

    id = Column(String(60), primary_key=True, nullable=False)
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)

    if models.storage_t == "db":
        places = relationship("Place", backref="cities")

    def __init__(self, *args, **kwargs):
        """initializes city"""
        super().__init__(*args, **kwargs)

    def __str__(self):
        """Returns a string representation of the City instance"""
        return "[City] ({}) {}".format(self.id, self.__dict__)
