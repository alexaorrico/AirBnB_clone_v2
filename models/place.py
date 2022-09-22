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
        reviews = relationship("Review", backref="place")
        amenities = relationship("Amenity", secondary="place_amenity",
                                 backref="place_amenities",
                                 viewonly=False)
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
        amenity_ids = []

    REQUIRED_ATTRS = ["name", "user_id"]
    SKIP_UPDATE_ATTRS = ["id",
                         "user_id",
                         "city_id",
                         "created_at",
                         "updated_at"]
    DICT_CLASSNAME_AND_SUB = {"name": "City",
                              "subtype": "places"}

    def __init__(self, *args, **kwargs):
        """initializes Place"""
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
            """getter attribute returns the list of Amenity instances"""
            from models.amenity import Amenity
            amenity_list = []
            all_amenities = models.storage.all(Amenity)
            for amenity in all_amenities.values():
                if amenity.place_id == self.id:
                    amenity_list.append(amenity)
            return amenity_list

    @classmethod
    def api_get_all(cls, idOfObject):
        """handles the API get command for all objects
        return a list Always, sometime empty.
        """
        from models.city import City
        City.ensure_objectId_is_valid(idOfObject)
        return (super(Place, cls).
                storage_retrieve_all_subtype(
                    idOfObject,
                    cls.DICT_CLASSNAME_AND_SUB))

    @classmethod
    def api_get_single(cls, idOfObject):
        """handles the API get command for specific object
        return Values: 200: success
        404: invalid object.
        """
        cls.ensure_objectId_is_valid(idOfObject)
        return (super(Place, cls).
                storage_retrieve_single(idOfObject))

    @classmethod
    def api_delete(cls, idOfObject):
        """handles the API delete command for all types
        return Values: empyt dictionary on success or
        raise exception
        """
        cls.ensure_objectId_is_valid(idOfObject)
        return (super(Place, cls).
                storage_delete_single(idOfObject))

    @classmethod
    def api_put(cls, putDataAsDict, idOfObject):
        """handles the API put command for all types
        Return Values: item dictionary or
        raise exception"""
        cls.ensure_objectId_is_valid(idOfObject)
        return (super(Place, cls).
                storage_update_item(putDataAsDict,
                                    idOfObject))

    @classmethod
    def api_post(cls, postDataAsDict, idOfObject):
        """handles the API post command for all types
        Return Values: newObject dictionary
        or Riase exception"""
        cls.api_post_data_verify(idOfObject, postDataAsDict)
        postDataAsDict["city_id"] = idOfObject
        return (super(Place, cls).
                storage_create_item(postDataAsDict))

    @classmethod
    def api_post_data_verify(cls, idOfObject, postData):
        """verifys data in post dictionary"""
        from models.city import City
        from models.user import User
        City.ensure_objectId_is_valid(idOfObject)
        cls.ensure_dict_is_correct_type(postData)
        cls.ensure_dict_contains_req_attrs(postData)
        User.ensure_objectId_is_valid(postData["user_id"])
