#!/usr/bin/python3
"""script that starts a Flask web application"""

from flask import Blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
