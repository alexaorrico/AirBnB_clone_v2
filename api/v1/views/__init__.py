#!/usr/bin/python3
""" view set up"""


from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
from . import index
from api.v1.views.cities import *
from . import users
from . import places_reviews
