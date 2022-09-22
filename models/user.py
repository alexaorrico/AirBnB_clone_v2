#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    REQUIRED_ATTRS = ["email", "password"]
    SKIP_UPDATE_ATTRS = ["id",
                         "email",
                         "created_at",
                         "updated_at"]

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    @classmethod
    def api_put(cls, putDataAsDict, idOfObject):
        """handles the API put command for all types
        Return Values: item dictionary or
        raise exception"""
        cls.ensure_objectId_is_valid(idOfObject)
        return (super(User, cls).
                storage_update_item(putDataAsDict,
                                    idOfObject))

    @classmethod
    def api_post(cls, postDataAsDict):
        """handles the API post command for all types
        Return Values: newObject dictionary
        or Riase exception"""
        return (super(User, cls).
                storage_create_item(postDataAsDict))

    @classmethod
    def api_delete(cls, idOfObject):
        """handles the API delete command for all types
        return Values: empyt dictionary on success or
        raise exception
        """
        cls.ensure_objectId_is_valid(idOfObject)
        return (super(User, cls).
                storage_delete_single(idOfObject))

    @classmethod
    def api_get_single(cls, idOfObject):
        """handles the API get command for specific object
        return Values: 200: success
        404: invalid object.
        """
        cls.ensure_objectId_is_valid(idOfObject)
        return (super(User, cls).
                storage_retrieve_single(idOfObject))

    @classmethod
    def api_get_all(cls):
        """handles the API get command for all objects
        return a list Always, sometime empty.
        """
        return (super(User, cls).
                storage_retrieve_all_type(cls))
