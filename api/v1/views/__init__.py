#!/usr/bin/python3
''' Creates blueprint for flask app which will
    be imported into app.py
'''
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix="/api/v1")
from api.v1.views.index import *
