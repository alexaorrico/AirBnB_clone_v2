#!/usr/bin/python3
""" import files  and set up a blueprint """
from flask import Blueprint

app_views = Blueprint('status', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places_reviews import *
from api.v1.views.places import *
from api.v1.views.places_amenities import *
