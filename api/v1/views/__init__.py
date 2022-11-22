#!/usr/bin/python3
"""
Registers Blueprints.
"""


# from api.v1.views.index import *
from flask import Blueprint


app_views = Blueprint('api_views', __name__, url_prefix="/api/v1")

from api.v1.views.index import *
