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
    def api_put(cls, listToIgnore, resuestDataAsDict, ObjToUpdate):
        """handles the API put command for all types
        Return Values: 200: Success
        404: invalid object
        400: invalid Json"""
        if not cls.test_request_data(resuestDataAsDict):
            return ({'error': 'Not a JSON'}, 400)
        if ObjToUpdate is None:
            return (None, 404)
        for key, value in resuestDataAsDict.items():
            if key in listToIgnore:
                continue
            setattr(ObjToUpdate, key, value)
        ObjToUpdate.save()
        return (ObjToUpdate.to_dict(), 200)

    @classmethod
    def api_post(cls, postDataAsDict):
        """handles the API post command for all types
        Return Values: newObject dictionary
        or Riase exception"""
        return (super(State, cls).
                storage_delete_single(postDataAsDict))

    @classmethod
    def test_request_data(cls, requestDataAsDict):
        """used to test if the request data is accurate."""
        if requestDataAsDict is None or type(requestDataAsDict) != dict:
            return (False)
        return (True)

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
