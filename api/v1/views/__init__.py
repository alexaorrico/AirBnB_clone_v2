#!/usr/bin/python3
"""
Contains a python script that creates a flask blueprint
named app_views as part of a larger flask application
contains the folllowing views: index, states, cities
amenities, uusers and places
"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
