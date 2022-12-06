#!/usr/bin/python3
"""Index file"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def app_views_status():
    """returns status"""
    dictionary = {"status": "OK"}
    return jsonify(dictionary)
