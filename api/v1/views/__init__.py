#!/bin/python3
"""initialize views package"""

# imports
from flask import Blueprint

# define a blueprint
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# avoid circular import
from api.v1.views.index import *
