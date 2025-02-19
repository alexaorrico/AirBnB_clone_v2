#!/usr/bin/python3
"""
State Class from Module
"""
import os
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
import models

# Determine the storage type
storage_type = os.getenv('HBNB_TYPE_STORAGE')

class State(BaseModel, Base):
    """State class handles all application states"""
    
    if storage_type == "db":
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship('City', backref='state', cascade='delete')
    else:
        name = ''

    if storage_type != 'db':
        @property
        def cities(self):
            """
            Getter method for cities when using file storage
            :return: List of City instances related to this State instance
            """
            return [city for city in models.storage.all("City").values() if city.state_id == self.id]
