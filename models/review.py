#!/usr/bin/python
""" holds class Review"""
from models.base_model import BaseModel


class Review(BaseModel):
    """Representation of Review """
    self.place_id = ""
    self.user_id = ""
    self.text = ""

    def __init__(self, *args, **kwargs):
        """initializes Review"""
        super().__init__(*args, **kwargs)
