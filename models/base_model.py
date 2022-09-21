#!/usr/bin/python3
"""
Contains class BaseModel
"""

from datetime import datetime
import re
import models
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid

time = "%Y-%m-%dT%H:%M:%S.%f"

if models.storage_t == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """The BaseModel class from which future classes will be derived"""
    if models.storage_t == "db":
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"], time)
            else:
                self.created_at = datetime.utcnow()
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            else:
                self.updated_at = datetime.utcnow()
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

    def __str__(self):
        """String representation of the BaseModel class"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)

    def save(self):
        """updates the attribute 'updated_at' with the current datetime"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(time)
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        return new_dict

    def delete(self):
        """delete the current instance from the storage"""
        models.storage.delete(self)

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
        return (newObjct.to_dict(), 200)

    @classmethod
    def append_id_to_dictionary(cls, resuestDataAsDict, objectId):
        """addends an ID to dictionary (Bad solution)"""
        classIdComparison = {"City":"state_id", "Place":"user_id", "Review":"user_id"}
        if cls.__name__ in classIdComparison.keys():
            resuestDataAsDict[classIdComparison[cls.__name__]] = objectId

    @classmethod
    def ensure_objectId_is_valid(cls, objectId):
        """checks the corisponding object ID"""
        classIdComparison = {"City":"State", "Place":"User", "Review":"User"}
        if objectId is not None and models.storage.get(classIdComparison[cls.__name__], objectId) is None:
            return (False)
        return (True)
    # @classmethod
    # def test_attribute_for_model(cls, attribute, objectId):
    #     """used to test if an attribute is a model"""
    #     arrayOfModels = ["Amenity", "City", "Place", "Review", "State", "User"]
    #     for modelName in arrayOfModels:
    #         if modelName.lower() in attribute.lower():
    #             if models.storage.get(cls, objectId) is not None:
    #                 print("\n\tin models.storage.get not None\n")
    #                 return (True)
    #             else:
    #                 print("\n\tin models.storage.get is None\n")
    #                 return (False)
    #     return (True)

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

    @staticmethod
    def api_get_single(ObjToRetrieve):
        """handles the API get command for specific object
        return Values: 200: success
        404: invalid object.
        """
        if ObjToRetrieve is None:
            return (None, 404)
        return (ObjToRetrieve.to_dict(), 200)

    @staticmethod
    def api_get_all(listOfObjsToRetrieve):
        """handles the API get command for all objects
        return Values: 200: success
        """
        if len(listOfObjsToRetrieve) == 0:
            return (None, 404)
        return ([obj.to_dict() for obj in listOfObjsToRetrieve], 200)
