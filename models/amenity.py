#!/usr/bin/python3
from models.base_model import BaseModel, Base, Table, Column, String
from os import getenv
from sqlalchemy.orm import relationship, backref
"""
amenity module
    contains
        the Amentiry class inherts from BaseModel and Base
"""


class Amenity(BaseModel, Base):
<<<<<<< HEAD
    """
    The Amenity class
    """
    if getenv('HBNB_TYPE_STORAGE', 'fs') == 'db':
        __tablename__ = 'amenities'
=======
    """Representation of Amenity """
    __tablename__ = 'amenities'
    if getenv("HBNB_TYPE_STORAGE") == "db":
>>>>>>> 0e125649dcfd402fd7b762fe147243315523b4f2
        name = Column(String(128), nullable=False)
#        place_amenities = relationship("PlaceAmenity", backref="amenity",
#                                       cascade="all, delete, delete-orphan")
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """
        initializes class objects. Inherits attributes from parent
        """
        super().__init__(*args, **kwargs)
