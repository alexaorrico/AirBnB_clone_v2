#!/usr/bin/python
""" holds class City"""
import imp
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """Representation of city """
    REQUIRED_ATTRS = ["name"]
    SKIP_UPDATE_ATTRS = ["id",
                         "state_id",
                         "created_at",
                         "updated_at"]
    DICT_CLASSNAME_AND_SUB = {"name": "State",
                              "subtype": "cities"}

    if models.storage_t == "db":
        __tablename__ = 'cities'
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        name = Column(String(128), nullable=False)
        places = relationship("Place", backref="cities")
    else:
        state_id = ""
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes city"""
        super().__init__(*args, **kwargs)

    @classmethod
    def api_get_all(cls, idOfObject):
        """handles the API get command for all objects
        return a list Always, sometime empty.
        """
        from models.state import State
        State.ensure_objectId_is_valid(idOfObject)
        return (super(City, cls).
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
        return (super(City, cls).
                storage_retrieve_single(idOfObject))

    @classmethod
    def api_delete(cls, idOfObject):
        """handles the API delete command for all types
        return Values: empyt dictionary on success or
        raise exception
        """
        cls.ensure_objectId_is_valid(idOfObject)
        return (super(City, cls).
                storage_delete_single(idOfObject))

    @classmethod
    def api_put(cls, putDataAsDict, idOfObject):
        """handles the API put command for all types
        Return Values: item dictionary or
        raise exception"""
        cls.ensure_objectId_is_valid(idOfObject)
        return (super(City, cls).
                storage_update_item(putDataAsDict,
                                    idOfObject))

    @classmethod
    def api_post(cls, postDataAsDict, idOfObject):
        """handles the API post command for all types
        Return Values: newObject dictionary
        or Riase exception"""
        cls.api_post_data_verify(idOfObject, postDataAsDict)
        postDataAsDict["state_id"] = idOfObject
        return (super(City, cls).
                storage_create_item(postDataAsDict))

    @classmethod
    def api_post_data_verify(cls, idOfObject, postData):
        """verifys data in post dictionary"""
        from models.state import State
        State.ensure_objectId_is_valid(idOfObject)
        cls.ensure_dict_is_correct_type(postData)
