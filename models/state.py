#!/usr/bin/python3
import models
from models.base_model import BaseModel, Base, Table, Column, String
from sqlalchemy.orm import relationship, backref
from os import getenv
"""
state module
    contain
        State class
"""


class State(BaseModel, Base):
    """
    This is the State class
    """
    if getenv('HBNB_TYPE_STORAGE', 'fs') == 'db':
        __tablename__ = "states"
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state",
                              cascade="all, delete, delete-orphan")
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """
        initializes from BaseModel Class
        """
        super(State, self).__init__(*args, **kwargs)

    if getenv('HBNB_TYPE_STORAGE', 'fs') != 'db':
        @property
        def cities(self):
            """
            returns all cities in a State
            """
            all_cities = models.storage.all("City").values()
            result = [city for city in all_cities if city.state_id == self.id]
            return result
