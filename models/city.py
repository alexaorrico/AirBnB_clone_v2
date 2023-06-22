#!/usr/bin/python3
"""This is the city class."""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import environ


class City(BaseModel, Base):
    """This is the class for City."""

    __tablename__ = "cities"
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
    if environ.get("HBNB_TYPE_STORAGE"):
        places = relationship(
            'Place', cascade='all, delete-orphan', backref='cities')
