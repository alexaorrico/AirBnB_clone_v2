#!/usr/bin/python3
"""
Review Class from Module
"""
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey

# Determine the storage type
storage_type = os.getenv('HBNB_TYPE_STORAGE')

class Review(BaseModel, Base):
    """Review class handles all reviews"""
    
    if storage_type == "db":
        __tablename__ = 'reviews'
        text = Column(String(1024), nullable=False)
        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    else:
        place_id = ''
        user_id = ''
        text = ''
