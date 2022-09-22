#!/usr/bin/python3
""" holds class State"""
import models
from models.base_model import BaseModel, Base
from models.city import City
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """Representation of state """
    if models.storage_t == "db":
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state")
    else:
        name = ""

    REQUIRED_ATTRS = ["name"]
    SKIP_UPDATE_ATTRS = ["id", "created_at", "updated_at"]

    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)

    if models.storage_t != "db":
        @property
        def cities(self):
            """getter for list of city instances related to the state"""
            city_list = []
            all_cities = models.storage.all(City)
            for city in all_cities.values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list

    @classmethod
    def api_put(cls, putDataAsDict, idOfObject):
        """handles the API put command for all types
        Return Values: item dictionary or
        raise exception"""
        return (super(State, cls).
                storage_update_item(putDataAsDict,
                                    idOfObject))

    @classmethod
    def api_post(cls, postDataAsDict):
        """handles the API post command for all types
        Return Values: newObject dictionary
        or Riase exception"""
        return (super(State, cls).
                storage_create_item(postDataAsDict))

    @classmethod
    def api_delete(cls, idOfObject):
        """handles the API delete command for all types
        return Values: empyt dictionary on success or 
        raise exception
        """
        return (super(State, cls).
                storage_delete_single(idOfObject))

    @classmethod
    def api_get_single(cls, idOfObject):
        """handles the API get command for specific object
        return Values: 200: success
        404: invalid object.
        """
        return (super(State, cls).
                storage_retrieve_single(idOfObject))

    @classmethod
    def api_get_all(cls):
        """handles the API get command for all objects
        return a list Always, sometime empty.
        """
        return (super(State, cls).
                storage_retrieve_all_type(cls))
