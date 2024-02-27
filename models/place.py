#!/usr/bin/python3
"""
Place Class from Models Module
"""
import os
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey,\
    MetaData, Table, ForeignKey
from sqlalchemy.orm import backref
STORAGE_TYPE = os.environ.get('HBNB_TYPE_STORAGE')

if STORAGE_TYPE == "db":
    class PlaceAmenity(Base):
        """ PlaceAmenity Class """
        __tablename__ = 'place_amenity'
        metadata = Base.metadata
        place_id = Column(String(60),
                          ForeignKey('places.id'),
                          nullable=False,
                          primary_key=True)
        amenity_id = Column(String(60),
                            ForeignKey('amenities.id'),
                            nullable=False,
                            primary_key=True)


class Place(BaseModel, Base):
    """Place class handles all application places"""
    if STORAGE_TYPE == "db":
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

        amenities = relationship('Amenity', secondary="place_amenity",
                                 viewonly=False)
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
        review_ids = []

        @property
        def amenities(self):
            """
                getter for amenitiess list, i.e. amenities attribute of self
            """
            if len(self.amenity_ids) > 0:
                return amenity_ids
            else:
                return None

        @amenities.setter
        def amenities(self, amenity_obj):
            """
                setter for amenity_ids
            """
            if amenity_obj and amenity_obj not in self.amenity_ids:
                self.amenity_ids.append(amenity_obj.id)

        @property
        def reviews(self):
            """
                getter for reviews list, i.e. reviews attribute of self
            """
            if len(self.review_ids) > 0:
                return review_ids
            else:
                return None

        @reviews.setter
        def reviews(self, review_obj):
            """
                setter for review_ids
            """
            if review_obj and review_obj not in self.review_ids:
                self.review_ids.append(review_obj.id)
