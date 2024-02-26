#!/usr/bin/python3
"""
defining the __init__file for api
"""


from flask import Blueprint
# from api.v1.views.index import *

app_views = Blueprint('/api/v1', __name__, url_prefix="/api/v1")

# Import the status route using the wildcard
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
