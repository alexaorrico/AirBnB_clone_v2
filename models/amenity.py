#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.place import place_amenity
import os


class Amenity(BaseModel, Base):
    __tablename__ = "amenities"
    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        place_amenities = relationship("Place",
                                       secondary=place_amenity,
                                       back_populates="amenities")
    else:
        name = ""
