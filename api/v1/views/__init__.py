#!/usr/bin/python3
"""
module that initializes the "app_views"
"""
from flask import register_blueprint


app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.views.index import *
