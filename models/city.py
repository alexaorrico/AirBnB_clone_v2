#!/usr/bin/python
""" holds class City"""
from os import getenv

import sqlalchemy
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

import models
from models.base_model import Base, BaseModel
from models.place import Place


class City(BaseModel, Base):
    """Representation of city """
    if models.storage_t == "db":
        __tablename__ = 'cities'
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        name = Column(String(128), nullable=False)
        places = relationship("Place", backref="cities")
    else:
        state_id = ""
        name = ""

        @property
        def places(self):
            """Get list of places that match this cities id"""
            return [
                v for _, v in models.storage.all(Place).items()
                if v.city_id == self.id
            ]

    def __init__(self, *args, **kwargs):
        """initializes city"""
        super().__init__(*args, **kwargs)
