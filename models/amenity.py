#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """The Amenity class inherits from the BaseModel and Base/
    classes in Python."""

    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)
