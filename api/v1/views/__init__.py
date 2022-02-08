#!/usr/bin/python3
"""
module that uses blueprint to generate app view
"""

from flask import Blueprint

app_views = Blueprint('app_view', __name__, url_prefix='/api/v1/')

from api.v1.views.index import *
from api.v1.views import states, cities, amenities, users
from api.v1.views import places, places_reviews
