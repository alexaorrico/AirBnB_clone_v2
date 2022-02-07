#!/usr/bin/python3
""""smth"""

from flask import Blueprint

app_views = Blueprint('__init__', __name__, url_prefix='/api/v1')


from api.views.index import *
from api.views.states import *
from api.views.cities import *
from api.views.amenities import *
from api.views.users import *
