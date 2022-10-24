#!/usr/bin/python3
"""contains app_views blueprint"""
from flask import Blueprint

app_views = Blueprint('api', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places_reviews import *
from api.v1.views.places import *
