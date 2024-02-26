#!/usr/bin/python3
"""Index Page"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", strict_slashes=False)
def get_status():
    """
    Route to return status in JSON format
    """
    data = {"status": "ok"}
    response = jsonify(data)
    return response


@app_views.route("/stats", methods=["GET"], strict_slashes=False)
def stats():
    """
    stats of all objs route
    :return: json of all objs
    """
    data = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
    }

    response = jsonify(data)
    resp.status_code = 200

    return response
