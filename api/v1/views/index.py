#!/usr/bin/python3
"""
returns the status of the app_views object at route /status
"""

from . import app_views
from models import storage
from flask.json import jsonify


@app_views.route("/status")
def status():
    return jsonify(status="OK")


@app_views.route("/stats")
def stats():
    """Get number of objects indexed by type"""
    return jsonify(
        amenities=storage.count("Amenity"),
        cities=storage.count("City"),
        places=storage.count("Place"),
        reviews=storage.count("Review"),
        states=storage.count("State"),
        users=storage.count("User"),
    )
