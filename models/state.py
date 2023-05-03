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
<<<<<<< HEAD
    """
    This is the State class
    """
    if getenv('HBNB_TYPE_STORAGE', 'fs') == 'db':
        __tablename__ = "states"
=======
    """Representation of state """
    __tablename__ = 'states'
    if getenv("HBNB_TYPE_STORAGE") == "db":
>>>>>>> 0e125649dcfd402fd7b762fe147243315523b4f2
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

<<<<<<< HEAD
    if getenv('HBNB_TYPE_STORAGE', 'fs') != 'db':
        @property
        def cities(self):
            """
            returns all cities in a State
            """
            all_cities = models.storage.all("City").values()
            result = [city for city in all_cities if city.state_id == self.id]
            return result
=======
    if getenv("HBNB_TYPE_STORAGE") == "db":
        @property
        def cities(self):
            """getter for list of city instances related to the state"""
            city_list = []
            all_cities = models.storage.all("City")
            for city in all_cities.values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
>>>>>>> 0e125649dcfd402fd7b762fe147243315523b4f2
