#!/usr/bin/python3
"""imports Blueprint from flask"""

from flask import Blueprint
# from api.v1.views.iindex import *

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.views.index import *
from api.v1.views.states import *
