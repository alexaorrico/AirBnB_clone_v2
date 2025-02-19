#!/usr/bin/python3
"""
Place Class from Module
"""
import os
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
import models

# Determine the storage type
storage_type = os.getenv('HBNB_TYPE_STORAGE')

if storage_type == "db":
    place_amenity = Table(
        'place_amenity', Base.metadata,
        Column('place_id', String(60), ForeignKey('places.id')),
        Column('amenity_id', String(60), ForeignKey('amenities.id', ondelete="CASCADE"))
    )

class Place(BaseModel, Base):
    """Place class handles all places"""
    
    if storage_type == "db":
        __tablename__ = 'places'
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        amenities = relationship('Amenity', secondary="place_amenity", viewonly=False)
        reviews = relationship('Review', backref='place', cascade='delete')
    else:
        city_id = ''
        user_id = ''
        name = ''
        description = ''
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

    if storage_type != "db":
        @property
        def amenities(self):
            """
            Amenities getter for file storage
            :return: List of Amenity instances related to this Place instance
            """
            return [models.storage.get("Amenity", a_id) for a_id in self.amenity_ids]

        @amenities.setter
        def amenities(self, amenity):
            """
            Amenities setter for file storage
            :param amenity: Amenity instance to add
            """
            if amenity and amenity.id not in self.amenity_ids:
                self.amenity_ids.append(amenity.id)

        @property
        def reviews(self):
            """
            Reviews getter for file storage
            :return: List of Review instances related to this Place instance
            """
            return [review for review in models.storage.all("Review").values() if review.place_id == self.id]

