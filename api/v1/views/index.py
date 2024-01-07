#!/usr/bin/python3
"""
  route in object that returns a json
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """
    Return the status of the API
    """
    return jsonify({"status": "OK"})
