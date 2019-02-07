#!/usr/bin/python3
""" initial blueprint for routing api views """
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

if app_views:
    from api.v1.views.index import *
    from api.v1.views import states
