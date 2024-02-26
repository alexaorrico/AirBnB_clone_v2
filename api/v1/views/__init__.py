#!/usr/bin/python3
"""The Flask blueprint for the API. """
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
"""The blueprint for the AirBnB API."""

from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.amenities import *
