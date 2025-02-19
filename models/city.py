#!/usr/bin/python3
"""
City Class from Module
"""
import os
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey
import models

# Determine the storage type
storage_type = os.getenv('HBNB_TYPE_STORAGE')

class City(BaseModel, Base):
    """City class handles all cities"""
    
    if storage_type == "db":
        __tablename__ = 'cities'
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        places = relationship('Place', backref='cities', cascade='delete')
    else:
        name = ''
        state_id = ''

    if storage_type != 'db':
        @property
        def places(self):
            """
            Getter for places when using file storage
            :return: List of Place instances related to this City instance
            """
            all_places = models.storage.all("Place")
            return [place for place in all_places.values() if place.city_id == self.id]
