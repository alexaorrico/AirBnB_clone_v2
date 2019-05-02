#!/usr/bin/python3
"""Init file for v1.views"""

from flask import Blueprint

app_views = Blueprint("views", __name__, url_prefix="/api/v1")

from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
