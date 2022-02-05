#!/usr/bin/python3
"""
Index for hbnb REST api
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def api_status():
    """returns status of the api"""
    return jsonify({"status": "OK"})
