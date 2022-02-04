#!/usr/bin/python3
"""
Script that starts a Flask web application
"""
from api.v1.views.index import *
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
