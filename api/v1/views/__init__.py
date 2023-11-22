#!/usr/bin/python3
""" Blueprint """
# Michael edited 11/22 9:29 AM

from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenity import *
from api.v1.views.user import *
from api.v1.views.place import *
