#!/usr/bin/python3
"""create ?
"""

from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from flask import Blueprint

app_views = Blueprint("app_view", __name__, url_prefix="/api/v1")
