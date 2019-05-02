#!/usr/bin/python3

from flask import Blueprint
app_views = Blueprint('app_voews', __name__, url_prefix="/api/v1")

from api.v1.views import *
from api.v1.views.cities import *
from api.v1.views.index import *
