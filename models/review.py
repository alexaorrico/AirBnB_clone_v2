#!/usr/bin/python
""" holds class Review"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey


class Review(BaseModel, Base):
    """Representation of Review """
    if models.storage_t == 'db':
        __tablename__ = 'reviews'
        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        text = Column(String(1024), nullable=False)
    else:
        place_id = ""
        user_id = ""
        text = ""

    REQUIRED_ATTRS = ["text", "user_id"]
    SKIP_UPDATE_ATTRS = ["id",
                         "user_id",
                         "place_id",
                         "created_at",
                         "updated_at"]
    DICT_CLASSNAME_AND_SUB = {"name": "Place",
                              "subtype": "reviews"}

    def __init__(self, *args, **kwargs):
        """initializes Review"""
        super().__init__(*args, **kwargs)

    @classmethod
    def api_get_all(cls, idOfObject):
        """handles the API get command for all objects
        return a list Always, sometime empty.
        """
        from models.place import Place
        Place.ensure_objectId_is_valid(idOfObject)
        return (super(Review, cls).
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
        return (super(Review, cls).
                storage_retrieve_single(idOfObject))

    @classmethod
    def api_delete(cls, idOfObject):
        """handles the API delete command for all types
        return Values: empyt dictionary on success or
        raise exception
        """
        cls.ensure_objectId_is_valid(idOfObject)
        return (super(Review, cls).
                storage_delete_single(idOfObject))

    @classmethod
    def api_put(cls, putDataAsDict, idOfObject):
        """handles the API put command for all types
        Return Values: item dictionary or
        raise exception"""
        cls.ensure_objectId_is_valid(idOfObject)
        return (super(Review, cls).
                storage_update_item(putDataAsDict,
                                    idOfObject))

    @classmethod
    def api_post(cls, postDataAsDict, idOfObject):
        """handles the API post command for all types
        Return Values: newObject dictionary
        or Riase exception"""
        cls.api_post_data_verify(idOfObject, postDataAsDict)
        postDataAsDict["place_id"] = idOfObject
        return (super(Review, cls).
                storage_create_item(postDataAsDict))

    @classmethod
    def api_post_data_verify(cls, idOfObject, postData):
        """verifys data in post dictionary"""
        from models.place import Place
        from models.user import User
        Place.ensure_objectId_is_valid(idOfObject)
        cls.ensure_dict_is_correct_type(postData)
        cls.ensure_dict_contains_req_attrs(postData)
        User.ensure_objectId_is_valid(postData["user_id"])
