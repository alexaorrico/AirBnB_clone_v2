#!/usr/bin/python
""" holds class Amenity"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """Representation of Amenity """
    if models.storage_t == 'db':
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
    else:
        name = ""

    REQUIRED_ATTRS = ["name"]
    SKIP_UPDATE_ATTRS = ["id",
                         "created_at",
                         "updated_at"]

    def __init__(self, *args, **kwargs):
        """initializes Amenity"""
        super().__init__(*args, **kwargs)

    @classmethod
    def api_put(cls, putDataAsDict, idOfObject):
        """handles the API put command for all types
        Return Values: item dictionary or
        raise exception"""
        cls.ensure_objectId_is_valid(idOfObject)
        return (super(Amenity, cls).
                storage_update_item(putDataAsDict,
                                    idOfObject))

    @classmethod
    def api_post(cls, postDataAsDict):
        """handles the API post command for all types
        Return Values: newObject dictionary
        or Riase exception"""
        return (super(Amenity, cls).
                storage_create_item(postDataAsDict))

    @classmethod
    def api_delete(cls, idOfObject):
        """handles the API delete command for all types
        return Values: empyt dictionary on success or 
        raise exception
        """
        cls.ensure_objectId_is_valid(idOfObject)
        return (super(Amenity, cls).
                storage_delete_single(idOfObject))

    @classmethod
    def api_get_single(cls, idOfObject):
        """handles the API get command for specific object
        return Values: 200: success
        404: invalid object.
        """
        cls.ensure_objectId_is_valid(idOfObject)
        return (super(Amenity, cls).
                storage_retrieve_single(idOfObject))

    @classmethod
    def api_get_all(cls):
        """handles the API get command for all objects
        return a list Always, sometime empty.
        """
        return (super(Amenity, cls).
                storage_retrieve_all_type(cls))
