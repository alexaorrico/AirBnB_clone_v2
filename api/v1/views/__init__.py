#!/usr/bin/python3
"""
This module defines a Flask Blueprint instance, app_views.

app_views is a Blueprint instance that is used to group related routes and
provide a URL prefix for these routes.
The URL prefix for app_views is '/api/v1'.
"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
