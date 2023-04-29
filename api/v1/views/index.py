#!/usr/bin/python3
"""
for rendering js content
"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status", strict_slashes=False)
def return_json():
    """return a json representation of an object
    """
    dictt = {"status": "OK"}
    return jsonify(dictt)
