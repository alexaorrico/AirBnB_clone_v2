#!/usr/bin/python3
"""
view Blueprint
"""
from flask import Blueprint


app_views = Blueprint('/api/v1', __name__, url_prefix='/api/v1')


# import views after the site has been defined
from api.v1.views.index import *

from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.states import *
