#!/usr/bin/python3
"""
for rendering js content
"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def return_json():
    """return a json representation of an object
    """
    return jsonify(status="Ok")
