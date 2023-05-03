#!/usr/bin/python3
from models.base_model import BaseModel, Base, Table, Column, String
from sqlalchemy import ForeignKey
from os import getenv
"""
review module
    contains
         Review class
"""


class Review(BaseModel, Base):
<<<<<<< HEAD
    """
    The review class
    """
    if getenv('HBNB_TYPE_STORAGE', 'fs') == 'db':
        __tablename__ = "reviews"
=======
    """Representation of Review """
    __tablename__ = 'reviews'
    if getenv("HBNB_TYPE_STORAGE") == "db":
>>>>>>> 0e125649dcfd402fd7b762fe147243315523b4f2
        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        text = Column(String(1024), nullable=False)
    else:
        place_id = ""
        user_id = ""
        text = ""

    def __init__(self, *args, **kwargs):
        """
        initialize from the BaseModel class
        """
        super().__init__(*args, **kwargs)
