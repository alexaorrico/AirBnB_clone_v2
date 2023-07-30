#!/usr/bin/python3
"""A init file"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
from api.v1.views.index import *
from api.v1.views.states import *

app_views.add_url_rule('/status', view_func=view_status)
app_views.add_url_rule('/stats', view_func=view_stats)
