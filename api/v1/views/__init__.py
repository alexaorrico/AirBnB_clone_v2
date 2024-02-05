"""
    creates an instance of blueprint plus
    a wild card import of everything in
    api.v1.views.index
"""
from flask import Blueprint

# Create a Blueprint instance with the specified URL prefix
app_views = Blueprint('app_views', __name__, url_prefix="/api/v1")

# Wildcard import for everything in api.v1.views.index, ignores PEP8 checks
from api.v1.views.index import *
