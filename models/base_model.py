#!/usr/bin/python3
"""
Defines the BaseModel class, the foundation for all models.
"""

import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
import models

time_format = "%Y-%m-%dT%H:%M:%S.%f"

# Determine whether to use a database or filesystem storage
if models.storage_t == "db":
    Base = declarative_base()
else:
    Base = object

class BaseModel(Base):
    """BaseModel class serves as the foundation for all model classes."""
    if models.storage_t == "db":
        id = Column(String(60), primary_key=True, nullable=False)
        created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
        updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, *args, **kwargs):
        """Initializes a BaseModel instance."""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            self.created_at = datetime.strptime(kwargs.get("created_at", datetime.utcnow().strftime(time_format)), time_format)
            self.updated_at = datetime.strptime(kwargs.get("updated_at", datetime.utcnow().strftime(time_format)), time_format)
            self.id = kwargs.get("id", str(uuid.uuid4()))
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.utcnow()

    def __str__(self):
        """Returns a string representation of the BaseModel instance."""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """Updates the 'updated_at' attribute with the current datetime."""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self, save_fs=None):
        """Returns a dictionary representation of the BaseModel instance."""
        new_dict = self.__dict__.copy()
        new_dict["created_at"] = self.created_at.strftime(time_format)
        new_dict["updated_at"] = self.updated_at.strftime(time_format)
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]

        # Hash the password to MD5 value if it exists
        if save_fs is None:
            new_dict.pop("password", None)

        return new_dict

    def delete(self):
        """Deletes the current instance from the storage."""
        models.storage.delete(self)
