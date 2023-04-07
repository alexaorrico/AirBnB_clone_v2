#!/usr/bin/python3
""" State Module for HBNB project """
import os

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.city import City
import models


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'

    name = Column(String(128), nullable=False)
    cities = relationship('City', backref='state',
                          cascade='all, delete-orphan')

    if os.getenv("HBNB_TYPE_STORAGE") != "db":
        # @property
        # def cities(self):
        #    """ list of city o=instances with state id"""
        #    all_cities = list(models.storage.all(City).values())
        #   return list(filter(lambda city: (city.id == self.id), all_cities)
        @property
        def cities(self):
            """ get list of city objects """
            city_list = []
            for city in models.storage.all(City).values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
