#!/usr/bin/python
""" holds class City"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    ''' The City Class '''
    __tablename__ = 'cities'

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        name = Column(String(128), nullable=False)
        state_id = Column(String(60),
                          ForeignKey('states.id', ondelete='CASCADE'),
                          nullable=False)
        places = relationship("Place", backref="cities", cascade="all, delete")
    else:
        name = ''
        state_id = ''
