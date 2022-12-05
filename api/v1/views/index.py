#!/usr/bin/python3
from api.v1.views import app_views

@app_views.route('/status', strict_slashes=False)
def index():
    """ok!"""
    return 'ok'

