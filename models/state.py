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
    def api_post(cls, listOfTestAttrs, resuestDataAsDict, objectId=None):
        """handles the API post command for all types
        Return Values: 200: Success
        404: missing Attribute
        400: invalid Json"""
        if not cls.test_request_data(resuestDataAsDict):
            return ({'error': 'Not a JSON'}, 400)
        if not cls.ensure_objectId_is_valid(objectId):
            return (None, 404)
        cls.append_id_to_dictionary(resuestDataAsDict, objectId)
        for attribute in listOfTestAttrs:
            if resuestDataAsDict.get(attribute) is None:
                return ({'error': 'Missing {}'.
                         format(attribute)}, 400)
        print(resuestDataAsDict)
        newObjct = cls(**resuestDataAsDict)
        newObjct.save()
        return (newObjct.to_dict(), 201)

    @classmethod
    def append_id_to_dictionary(cls, resuestDataAsDict, objectId):
        """addends an ID to dictionary (Bad solution)"""
        classIdComparison = {"City": "state_id",
                             "Place": "user_id",
                             "Review": "user_id"}
        if cls.__name__ in classIdComparison.keys():
            resuestDataAsDict[classIdComparison[cls.__name__]] = objectId

    @classmethod
    def ensure_objectId_is_valid(cls, objectId):
        """checks the corisponding object ID"""
        classIdComparison = {"City": "State",
                             "Place": "User",
                             "Review": "User"}
        if objectId is not None and models.storage.get(
                classIdComparison[cls.__name__], objectId) is None:
            return (False)
        return (True)

    @classmethod
    def test_request_data(cls, requestDataAsDict):
        """used to test if the request data is accurate."""
        if requestDataAsDict is None or type(requestDataAsDict) != dict:
            return (False)
        return (True)

    @staticmethod
    def api_delete(objectToDelete):
        """handles the API delete command for all types
        return Values: 200: success
        404: invalid object.
        """
        if objectToDelete is None:
            return (None, 404)
        objectToDelete.delete()
        return ({}, 200)

    @classmethod
    def api_get_single(cls, idOfObject):
        """handles the API get command for specific object
        return Values: 200: success
        404: invalid object.
        """
        return (BaseModel.storage_retrieve_single(idOfObject))

    @classmethod
    def api_get_all(cls):
        """handles the API get command for all objects
        return a list Always, sometime empty.
        """
        BaseModel.storage_retrieve_all_type(cls)
