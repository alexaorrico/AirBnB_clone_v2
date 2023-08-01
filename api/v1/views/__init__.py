#!/usr/bin/python3
"""This is an init file for blueprint"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views import states, cities, users, places, places_reviews
from api.v1.views.places_amenities import *
from api.v1.views import amenities
