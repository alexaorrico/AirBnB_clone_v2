#!/usr/bin/python3
"""will creates app_views a Flask Blueprint with a URL prefix"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
