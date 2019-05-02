#!/usr/bin/python3
"""Initializes module"""
from flask import Blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
from api.v1.views.index import *
from models.state import State
from api.v1.views.states import *
from models.city import City
from api.v1.views.cities import *
from models.amenity import Amenity
from api.v1.views.amenities import *
from models.user import User
from api.v1.views.users import *
from models.place import Place
from api.v1.views.places import *
from models.review import Review
from api.v1.views.places_reviews import *
