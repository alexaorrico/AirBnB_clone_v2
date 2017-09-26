#!/usr/bin/python
""" holds class Amenity"""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """Representation of Amenity """
    def __init__(self, *args, **kwargs):
        """initializes Amenity"""
        if len(kwargs) == 0:
            self.name = ""
        super().__init__(*args, **kwargs)
