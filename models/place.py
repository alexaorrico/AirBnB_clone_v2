#!/usr/bin/python3
"""
place module
    contains
        PlaceAmenity inherts from Base
            used to link table places and amenities
        Place inherts from BaseModel and Base
"""
import models
from models.base_model import BaseModel, Base, Table, Column
from os import getenv
from sqlalchemy import ForeignKey, String, Integer, Float
from sqlalchemy.orm import relationship, backref


# class PlaceAmenity(Base):
#     """
#     PlaceAmenity class designed to link table places and table amenities
#     of the SQLAlchmeny
#     """
#     if getenv('HBNB_TYPE_STORAGE', 'fs') == 'db':
#         __tablename__ = "place_amenity"
#         place_id = Column(String(60),
#                           ForeignKey('places.id'),
#                           primary_key=True, nullable=False)
#         amenity_id = Column(String(60), ForeignKey('amenities.id'),
#                             primary_key=True, nullable=False)


if getenv('HBNB_TYPE_STORAGE', 'fs') == 'db':
    place_amenity = Table("place_amenity", Base.metadata,
                          Column("place_id", String(60),
                                 ForeignKey('places.id'),
                                 primary_key=True, nullable=False),
                          Column("amenity_id", String(60),
                                 ForeignKey('amenities.id'),
                                 primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """
    Place Class
    """
    if getenv('HBNB_TYPE_STORAGE', 'fs') == 'db':
        __tablename__ = "places"
        city_id = Column(String(60),
                         ForeignKey('cities.id'),
                         nullable=False)
        user_id = Column(String(60),
                         ForeignKey('users.id'),
                         nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, default=0, nullable=False)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Integer, default=0, nullable=False)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        amenities = relationship("Amenity", secondary="place_amenity",
                                 backref="places")
        # no view_only=True
#        place_amenities = relationship("PlaceAmenity", backref="place",
#                              cascade="all, delete, delete-orphan")
        reviews = relationship("Review", backref="place",
                               cascade="all, delete, delete-orphan")
        __mapper_args__ = {"confirm_deleted_rows": False}
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenities_id = []

    def __init__(self, *args, **kwargs):
        """
        initializes the Place Class instance
        Inherts from BaseClass
        """
        super().__init__(*args, **kwargs)

    if getenv('HBNB_TYPE_STORAGE', 'fs') != 'db':
        @property
        def reviews(self):
            """
            lists all reviews for a place
            """
            all_reviews = models.storage.all("Review").values()
            result = [r for r in all_reviews if r.place_id == self.id]
            return result

    if getenv('HBNB_TYPE_STORAGE', 'fs') != 'db':
        @property
        def amenities(self):
            """
            lists all amenities for a place
            """
            result = []
            for a in self.amenities_id:
                b = models.storage.get("Amenity", a)
                if b is not None:
                    result.append(b)
            return result
