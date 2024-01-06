#!/usr/bin/python3
"""initialize view module"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")
from . import index
from api.v1.views import states
from api.v1.views import amenities
