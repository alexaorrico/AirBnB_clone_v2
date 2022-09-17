#!/usr/bin/python3
""""""
import json
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    """Returns a JSON"""
    return json({"status": "OK"})
