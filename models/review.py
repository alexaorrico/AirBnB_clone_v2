#!/usr/bin/python3
""" Review module for the HBNB project """
from sqlalchemy import Column, ForeignKey, String

from models.base_model import Base, BaseModel


class Review(BaseModel, Base):
    """
    Review class to store review information

    :param text: (str) The review description
    :param place_id: (str) The place id
    :param user_id: (str) The user id
    """
    __tablename__ = 'reviews'
    text = Column(String(1024), nullable=False)
    place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
