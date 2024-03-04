#!/usr/bin/python3
"""index page"""
from api.v1.views import app_views
from flask import jsonify
from models import storage, Amenity, City, Place, Review, State, User


@app_views.route("/status", strict_slashes=False)
def status():
    """return: status ok"""
    return jsonify({"status": "OK"})
