#!/usr/bin/python3
"""
index
"""
from flask import jsonify 
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    """return status json"""
    return jsonify(status="OK")