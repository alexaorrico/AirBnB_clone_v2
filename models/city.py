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
        stateRequested = models.storage.get("State", idOfObject)
        return (super(City, cls).
                storage_retrieve_all_type(
                    stateRequested.cities))
