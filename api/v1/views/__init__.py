#!/usr/bin/python3
"""
Contains the blueprint for the API
"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
<<<<<<< HEAD
=======
from api.v1.views.places_reviews import *
from api.v1.views.places_amenities import *
>>>>>>> 7612747aa7ee76fbc856f9194eddf49ee9ebe535
