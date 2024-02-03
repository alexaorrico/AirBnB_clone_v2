#!/usr/bin/python3
"""
innit file
"""


from flask import Blueprint
from api.v1.views import index
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
