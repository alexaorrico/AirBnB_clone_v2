#!usr/bin/python3
"""init file for views in REST API
"""
from flask import Blueprint
from api.v1.views.index import *
app_views = Blueprint('app_views', url_prefix='/app/v1')
