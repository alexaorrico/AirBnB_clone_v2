#!/usr/bin/python3
"""create blueprint"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Import views from submodules
from . import index
from . import states
from . import cities
from . import amenities
from . import users
from . import places
from . import places_reviews
from . import places_amenities
