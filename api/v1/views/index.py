#!/usr/bin/python3
"""returning status of the api"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    """
    The function "status" returns a JSON object
    with the key "status" set to "ok".
    """
    arg = {
        "status": "OK"
          }
    return jsonify(**arg)

@app_views.route('/stats', methods=["GET"])
def stats():
    """Return /status api route"""
    d = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User"
    }
    d = {k: storage.count(v) for k, v in d.items()}
    return jsonify(d)
