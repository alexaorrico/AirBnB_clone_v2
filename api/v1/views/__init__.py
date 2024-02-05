#!/usr/bin/python3
"""Blue print for flask document"""
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.reviews import *

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
