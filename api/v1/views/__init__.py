#!/usr/bin/python3
"""module"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Wildcard import for views in this package
from api.v1.views.index import *
