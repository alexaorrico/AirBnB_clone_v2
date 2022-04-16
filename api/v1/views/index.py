#!/usr/bin/python3
"""create a response form JSON file with the necessary modules"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def return_response():
    """return the response status in form of json structure"""
    return jsonify(status="OK")
