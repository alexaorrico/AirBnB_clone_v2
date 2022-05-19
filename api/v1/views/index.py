#!/usr/bin/python3
"""
    link db to api
"""
from api.v1.views import app_views
from models import storage
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """
        return satus of the api
    """
    return jsonify({"status": "OK"})
