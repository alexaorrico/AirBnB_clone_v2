#!/usr/bin/python3
"""API v1 view."""
from flask import Blueprint

app_views = Blueprint("/api/v1", __name__)

from api.v1.views.index import *
