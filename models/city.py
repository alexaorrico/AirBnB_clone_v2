#!/usr/bin/python
""" holds class City"""
from models.base_model import BaseModel


class City(BaseModel):
    """Representation of city """
    def __init__(self, *args, **kwargs):
        """initializes city"""
        if len(kwargs) == 0:
            self.name = ""
            self.state_id = ""
        super().__init__(*args, **kwargs)
