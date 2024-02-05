#!/usr/bin/python3
'''Contains the blueprint for the API.'''
# import Blueprint from flask
from flask import Blueprint
from api.v1.views.amenities import *
from api.v1.views.cities import *
from api.v1.views.index import *
from api.v1.views.places_amenities import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.states import *
from api.v1.views.users import *


# create a variable app_views which is an instance of Blueprint
# url prefix must be /api/v1
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
'''The blueprint for the AirBnB clone API.'''
