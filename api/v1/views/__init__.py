#!/usr/bin/python3
"""
The init file
"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix='/api/v1')


"""import storage packages"""
from models import storage
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity

"""Now import flask views"""
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.places_amenities import *
