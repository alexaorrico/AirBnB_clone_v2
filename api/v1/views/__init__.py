#!/usr/bin/python3
"""This module imports all from the app_views index"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
