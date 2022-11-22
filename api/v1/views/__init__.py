#!/usr/bin/python3
"""
Registers Blueprints.
"""

from flask import Blueprint


app_views = Blueprint('api_views', __name__)

from api.v1.views.index import *
