""" Holds class Amenity """
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

import models
from models.base_model import BaseModel, Base


class Amenity(BaseModel, Base):
    """ Amenity class represents amenities available in accommodations.

    Attributes:
        name (str): The name of the amenity.
    """
    if models.storage_t == 'db':
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """ Initializes Amenity """
        super().__init__(*args, **kwargs)
