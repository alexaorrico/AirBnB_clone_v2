#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import Column, String
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
import os
import models


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state",
                              cascade="all, delete-orphan")
    else:
        name = ""

        @property
        def cities(self):
            FLcity = models.storage.all(models.classes['City']).values()
            return [city for city in FLcity if city.state_id == self.id]
