#!/usr/bin/python3
"""
This module defines a route status for a Flask application using a Blueprint.
"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def hbnb_status():
    """
    This function is linked to the '/status' route.
    It returns a JSON object with the status of the API.
    """
    return jsonify({'status': 'OK'})
