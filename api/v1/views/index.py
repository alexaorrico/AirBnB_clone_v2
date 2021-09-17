#!/usr/bin/python3
"""
Views' index file
"""

from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def jsonify_app():
    """ Function that returns a JSON """
    return jsonify({"status": "OK"})
