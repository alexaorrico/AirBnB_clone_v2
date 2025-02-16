#!/usr/bin/python3
"""Blueprint for API"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Import all views (PEP8 will complain, ignore it)
from api.v1.views.index import *


