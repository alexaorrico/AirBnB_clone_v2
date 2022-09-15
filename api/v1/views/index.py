#!/usr/bin/python3
"""Index module"""
from api.v1.views import app_views
import json


@app_views.route('/status')
def index():
    """index page"""
    return json.dumps({"status": "OK"}, indent=4)
