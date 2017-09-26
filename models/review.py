#!/usr/bin/python
""" holds class Review"""
from models.base_model import BaseModel


class Review(BaseModel):
    """Representation of Review """
    def __init__(self, *args, **kwargs):
        """initializes Review"""
        if len(kwargs) == 0:
            self.place_id = ""
            self.user_id = ""
            self.text = ""
        super().__init__(*args, **kwargs)
