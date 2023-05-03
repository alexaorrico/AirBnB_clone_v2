#!/usr/bin/python3
from flask import Blueprint
from models.amenity import Amenity
from models.city import City
from models import storage
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.cities import *
from api.v1.views.places import *
from api.v1.views.places_amenities import *
from api.v1.views.places_reviews import *
"""
creates the Blueprint for flask application
"""
# this means a client querying dns/api/v1/ will be handled by
# api_views
# and all those routes are inside the __name__ ie here views module
