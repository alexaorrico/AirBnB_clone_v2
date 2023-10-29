#!/usr/bin/python
""" holds class Place"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

if models.storage_t == 'db':
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id', onupdate='CASCADE',
                                            ondelete='CASCADE'),
                                 primary_key=True),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id', onupdate='CASCADE',
                                            ondelete='CASCADE'),
                                 primary_key=True))


class Place(BaseModel, Base):
    """Representation of Place """
    if models.storage_t == 'db':
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
        reviews = relationship("Review", backref="place",
                               cascade='all, delete-orphan')
        amenities = relationship("Amenity", secondary="place_amenity",
                                 backref="place_amenities", viewonly=False)
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
        # amenity_ids = []  # moved to __init__()

    def __init__(self, *args, **kwargs):
        """initializes Place"""
    # amenity_ids forced to be an instance attribute since it is not necessarly
    # +passed as a key word argument upon first instantiation like others which
    # +would have made it an instance attribute. This way its present in
    # +self.__dict__ and its state can be saved in filestorage mode. Its popped
    # +in BaseModel.to_dict(mode=None) if mode is not file_save. But visible in
    # +methods that call self.__dict__ directly like BaseModel.str().
        if models.storage_t != 'db':
            self.amenity_ids = []
        super().__init__(*args, **kwargs)

    if models.storage_t != 'db':
        @property
        def reviews(self):
            """getter attribute returns the list of Review instances"""
            from models.review import Review
            review_list = []
            all_reviews = models.storage.all(Review)
            for review in all_reviews.values():
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list

        @property
        def amenities(self):
            """returns the list of 'Amenity' instances
            associated with place instance"""
            from models.amenity import Amenity
            all_amenities = models.storage.all(Amenity).values()
            return [amenity for amenity in all_amenities
                    if amenity.id in self.amenity_ids]

        @amenities.setter
        def amenities(self, amenity):
            from models.amenity import Amenity
            """associates amenity to place instance"""
            if type(amenity) is Amenity and amenity.id not in self.amenity_ids:
                self.amenity_ids.append(amenity.id)
