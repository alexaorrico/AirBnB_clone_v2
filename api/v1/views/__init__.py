#!/usr/bin/python3
"""
    setup the views for v1 api
"""

from api.v1.views.index import *
from flask import Blueprint

app_views = Blueprint('/api/v1/app_views', __name__)
