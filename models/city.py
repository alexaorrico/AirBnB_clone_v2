#!/usr/bin/python
""" holds class City"""
import models
from models.base_model import BaseModel, Base
from models.place import Place
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """Blueprint of the City Class"""
    if models.storage_t == "db":
        __tablename__ = 'cities'
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        name = Column(String(128), nullable=False)
        places = relationship("Place", backref="cities",
                              cascade='all, delete-orphan')
    else:
        state_id = ""
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes city"""
        super().__init__(*args, **kwargs)

    if models.storage_t != "db":
        @property
        def places(self):
            """getter for list of place instances related to the city"""
            place_list = [place for place in models.storage.all(Place).values()
                          if place.city_id == self.id]
            return place_list
