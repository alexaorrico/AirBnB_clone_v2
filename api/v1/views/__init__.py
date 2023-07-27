""" init file for views module
"""
from flask import Blueprint

app_views = Blueprint('views', __name__, url_prefix="/api/v1")

from api.v1.views.index import *
from api.v1.views import (amenities, cities, places, places_amenities,
                          places_reviews, states, users)
