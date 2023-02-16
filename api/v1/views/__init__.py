#!/usr/bin/python3
"""
This module creates the Flask Blueprint app_views\
        for the API routes for version 1.

The Blueprint app_views is created here and \
        the API routes for version 1 are imported here.

Usage:
    The Blueprint app_views can be registered \
            with a Flask application instance to
    expose the API routes for version 1.\
            See api.v1.app for an example.

import the necessary api routes
"""
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from flask import Blueprint
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *



# creation of Blueprint app_views
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")
