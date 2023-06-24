#!/usr/bin/python3
"""
Index module.

"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


app_views.route("/status", url_prefix='/api/v1')


def get_status():
    """Status of api."""
    return jsonify(status="ok")


@app_views.route('/stats', methods=['GET'])
def get_stats():
    """Retrieve the number of each objects by type."""
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(stats)
