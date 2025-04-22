#!/usr/bin/python3
"""creates blueprints for various views"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
states_views = Blueprint('states_views', __name__, url_prefix='/api/v1')
cities_views = Blueprint('cities_views', __name__, url_prefix='/api/v1')
amenities_views = Blueprint('amenities_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
