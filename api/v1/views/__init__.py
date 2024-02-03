#!/usr/bin/python3
"""
Initialize views
"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# PEP8 will complain about wildcard import here, but it is needed to make the
# endpoints accessible.
from api.v1.views.index import *

