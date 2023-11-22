#!/usr/bin/python3
"""Index script"""

from models import storage
from flask import jsonify

from api.v1.views import app_views
@app_views.route("/status")
def status():
    """Retrieve the status of the API"""
    return jsonify({"status": "OK"})

from api.v1.views import app_views
@app_views.route("/stats")
def objects():
    """Retrieve statistics on various objects"""
    from api.v1.views import app_views
    return jsonify({
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    })
