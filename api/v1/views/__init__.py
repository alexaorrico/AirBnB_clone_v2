#!/bin/python3
"""initialize views pacage"""

# imports
from flask import Blueprint
from api.v1.views.index import *

# define a blueprint
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")
