#!/usr/bin/python3
"""
BaseModel Class of Models Module
"""

import os
import json
import models
from uuid import uuid4, UUID
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime

STORAGE_TYPE = os.environ.get('HBNB_TYPE_STORAGE')

"""
    Creates instance of Base if storage type is a database
    If not database storage, uses class Base
"""
if STORAGE_TYPE == 'db':
    Base = declarative_base()
else:
    class Base:
        pass


class BaseModel:
    """
        attributes and functions for BaseModel class
    """

    if STORAGE_TYPE == 'db':
        id = Column(String(60), nullable=False, primary_key=True)
        created_at = Column(DateTime, nullable=False,
                            default=datetime.utcnow())
        updated_at = Column(DateTime, nullable=False,
                            default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """
            instantiation of new BaseModel Class
        """
        if kwargs:
            self.__set_attributes(kwargs)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()

    def __set_attributes(self, attr_dict):
        """
            private: converts attr_dict values to python class attributes
        """
        if 'id' not in attr_dict:
            attr_dict['id'] = str(uuid4())
        if 'created_at' not in attr_dict:
            attr_dict['created_at'] = datetime.utcnow()
        elif not isinstance(attr_dict['created_at'], datetime):
            attr_dict['created_at'] = datetime.strptime(
                attr_dict['created_at'], "%Y-%m-%d %H:%M:%S.%f")
        if 'updated_at' not in attr_dict:
            attr_dict['updated_at'] = datetime.utcnow()
        if 'updated_at' in attr_dict:
            if not isinstance(attr_dict['updated_at'], datetime):
                attr_dict['updated_at'] = datetime.strptime(
                    attr_dict['updated_at'], "%Y-%m-%d %H:%M:%S.%f")
        if STORAGE_TYPE != 'db' and '__class__' in attr_dict:
            del attr_dict['__class__']
        for attr, val in attr_dict.items():
            setattr(self, attr, val)

    def __is_serializable(self, obj_v):
        """
            private: checks if object is serializable
        """
        try:
            obj_to_str = json.dumps(obj_v)
            return obj_to_str is not None and isinstance(obj_to_str, str)
        except:
            return False

    def bm_update(self, attr_dict=None):
        """
            updates the basemodel and sets the correct attributes
        """
        if attr_dict:
            for key, value in attr_dict.items():
                setattr(self, key, value)
            self.save()

    def save(self):
        """
            updates attribute updated_at to current time
        """
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_json(self):
        """
            returns json representation of self
        """
        bm_dict = {}
        for key, val in (self.__dict__).items():
            if (self.__is_serializable(val)):
                bm_dict[key] = val
            else:
                bm_dict[key] = str(val)
        bm_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in bm_dict:
            del bm_dict["_sa_instance_state"]
        return(bm_dict)

    def __str__(self):
        """
            returns string type representation of object instance
        """
        class_name = type(self).__name__
        return '[{}] ({}) {}'.format(class_name, self.id, self.__dict__)

    def delete(self):
        """
            deletes current instance from storage
        """
        models.storage.delete(self)
