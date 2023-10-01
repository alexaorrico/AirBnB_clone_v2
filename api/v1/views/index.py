#!/usr/bin/python3
"""index.py"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def show_status():
    """returns a JSON string of the status in a 200 response"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def getstats():
    """retrieves the number of each objects by type"""
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
        }
    return jsonify(stats)


if __name__ == "__main__":
    pass
