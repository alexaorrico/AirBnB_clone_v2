#!/usr/bin/python3
""" script to create Blueprint app_views"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix="/api/v1")

# imports that ensure routes are registerd with app_views bp
from api.v1.views import index
from api.v1.views import states
from api.v1.views import cities
from api.v1.views import amenities
from api.v1.views import users
from api.v1.views import places
from api.v1.views.places_reviews import *
