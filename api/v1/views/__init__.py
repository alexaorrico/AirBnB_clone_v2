#!/usr/bin/python3
<<<<<<< HEAD

"""
creating blueprints for app.views
"""
=======
"""Contains Blueprint object"""
>>>>>>> 6338784aeb158049a5574267bcaba8774a776573

from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.views.index import *
<<<<<<< HEAD
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.places_amenities import *
=======
>>>>>>> 6338784aeb158049a5574267bcaba8774a776573
