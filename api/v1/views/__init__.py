#!/usr/bin/python3
"""
initializes the api views from a flask blueprint set up in api/v1/app.py
"""

from flask import Blueprint


app_views = Blueprint('index', __name__, url_prefix='/api/v1')
