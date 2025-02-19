#!/usr/bin/python3
"""
BaseModel Class of Module
"""

import os
import json
import models
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime

# Determine the storage type
storage_type = os.getenv('HBNB_TYPE_STORAGE')

# Base class definition based on storage type
Base = declarative_base() if storage_type == 'db' else type('Base', (object,), {})

class BaseModel:
    """
    Base class for all models, with shared attributes and methods
    """
    if storage_type == 'db':
        id = Column(String(60), nullable=False, primary_key=True)
        created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
        updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel instance"""
        self.id = str(uuid4())
        self.created_at = datetime.now()
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)

    def __is_serializable(self, obj_v):
        """
        Check if an object is serializable
        """
        try:
            json.dumps(obj_v)
            return True
        except TypeError:
            return False

    def bm_update(self, name, value):
        """
        Update the BaseModel instance with a new attribute value
        """
        setattr(self, name, value)
        if storage_type != 'db':
            self.save()

    def save(self):
        """Update 'updated_at' attribute and save the instance"""
        if storage_type != 'db':
            self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_json(self):
        """Return a JSON representation of the instance"""
        bm_dict = {key: value if self.__is_serializable(value) else str(value)
                   for key, value in self.__dict__.items()}
        bm_dict['__class__'] = type(self).__name__
        bm_dict.pop('_sa_instance_state', None)
        if storage_type == "db" and 'password' in bm_dict:
            bm_dict.pop('password')
        return bm_dict

    def __str__(self):
        """Return a string representation of the instance"""
        class_name = type(self).__name__
        return f'[{class_name}] ({self.id}) {self.__dict__}'

    def delete(self):
        """Delete the current instance from storage"""
        models.storage.delete(self)
