#!/usr/bin/python3
""" Init file for api/v1/views. """
from flask import Blueprint

app_views = Blueprint('simple_page', __name__, url_prefix='/api/v1')

from api.v1.views.amenities import *
from api.v1.views.cities import *
from api.v1.views.index import *
from api.v1.views.places import *
from api.v1.views.reviews import *
from api.v1.views.states import *
from api.v1.views.users import *
