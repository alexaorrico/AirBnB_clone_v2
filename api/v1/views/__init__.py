#!/usr/bin/python3

"""
Module: __init__ - initializes the views folder
"""
# order matters: the Blueprint instance must be defined
# before importing everything from index

from flask import Blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
from models import storage
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.amenities import *
from api.v1.views.places_reviews import *
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
