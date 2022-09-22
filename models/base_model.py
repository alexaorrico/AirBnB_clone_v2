#!/usr/bin/python3
"""
Contains class BaseModel
"""

from datetime import datetime
import models
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid

from models.exceptions import *

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
    def storage_update_item(cls, updateDataAsDict, idOfObject):
        """handles updating an item for storage
        """
        cls.ensure_dict_is_correct_type(updateDataAsDict)
        return (cls.update_object_from_dictionary(
            models.storage.get(cls, idOfObject),
            updateDataAsDict).
            to_dict())

    @classmethod
    def storage_create_item(cls, resuestDataAsDict):
        """handles creating a new time for storage
        """
        cls.ensure_dict_is_correct_type(resuestDataAsDict)
        cls.ensure_dict_contains_req_attrs(resuestDataAsDict)
        newObjct = cls(**resuestDataAsDict)
        newObjct.save()
        return (newObjct.to_dict())

    @classmethod
    def storage_delete_single(cls, idOfObject):
        """handles the delete command for a single
        object of any type from storage\n
        Does NOT verify Id Of Object, must be verified
        before passing
        """
        models.storage.get(cls, idOfObject).delete()
        models.storage.save()
        return ({})

    @classmethod
    def storage_retrieve_single(cls, idOfObject):
        """handles the return of a single object from
        storage
        """
        return (models.storage.get(cls, idOfObject).to_dict())

    @staticmethod
    def storage_retrieve_all_type(typeOfObjsToRetrieve):
        """handles the return of a single type from
        storage
        """
        retrievedObjects = models.storage.all(
                        typeOfObjsToRetrieve)
        return ([obj.to_dict()
                 for obj in retrievedObjects.values()])

    @classmethod
    def storage_retrieve_all_subtype(cls, idOfObject, ObjectInfoToRetrieve):
        """handles the return of a single type from
        storage
        Pass 2 parameters\n
        (valid Id of object) <- not checked in this method,\n
        (ObjectInfoToRetrieve) is a dictionary with the following
        format:\n
        {
            "name": "classType",
            "subtype": "subType"
        }
        """
        cls.ensure_dict_is_correct_type(ObjectInfoToRetrieve)
        retrievedObjects = getattr(
            models.storage.get(ObjectInfoToRetrieve["name"],
                               idOfObject),
            ObjectInfoToRetrieve["subtype"])
        return ([obj.to_dict()
                 for obj in retrievedObjects])

    @classmethod
    def update_object_from_dictionary(cls, objToUpdate, dictOfAttrs):
        """updates a verified object from a dictionary"""
        for attr, value in dictOfAttrs.items():
            if attr not in cls.SKIP_UPDATE_ATTRS:
                setattr(objToUpdate, attr, value)
        objToUpdate.save()
        return (objToUpdate)

    @classmethod
    def ensure_objectId_is_valid(cls, idOfObject):
        """checks the corisponding object ID"""
        print(idOfObject)
        if models.storage.get(cls, idOfObject) is None:
            raise BaseModelInvalidObject(idOfObject)

    @classmethod
    def ensure_dict_contains_req_attrs(cls, dictToTest):
        """tests the dictionary agains required attrs"""
        for attribute in cls.REQUIRED_ATTRS:
            if dictToTest.get(attribute) is None:
                raise BaseModelMissingAttribute(attribute)

    @classmethod
    def ensure_dict_is_correct_type(cls, dictToTest):
        """tests that the dictionary is a dictionary"""
        if dictToTest is None or type(dictToTest) != dict:
            raise BaseModelInvalidDataDictionary(dictToTest)
