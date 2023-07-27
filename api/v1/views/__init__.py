#!/usr/bin/python3
"""
File to make views a package for Flask API
"""
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


from api.v1.views.index import *
