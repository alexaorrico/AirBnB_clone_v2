#!/usr/bin/python
""" holds class State"""
from models.base_model import BaseModel


class State(BaseModel):
    """Representation of state """
    def __init__(self, *args, **kwargs):
        """initializes state"""
        if len(kwargs) == 0:
            self.name = ""
        super().__init__(*args, **kwargs)
