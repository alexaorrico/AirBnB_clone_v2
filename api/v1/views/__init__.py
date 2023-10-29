#!/usr/bin/python3
"""run flask server"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
if 1:
    from api.v1.views.index import *
    from api.v1.views.states import *
