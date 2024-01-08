#!/usr/bin/python3
"""initialize view module"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")
from . import index
from . import cities
from . import users
from . import states
from . import amenities
from . import places
from . import review
