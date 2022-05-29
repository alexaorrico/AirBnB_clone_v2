#!/usr/bin/python3
"""
import app_views and create a route /status
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status_route():
    """returns a JSON: "status": "OK" """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def gstats():
    """Gets stats for models  """
    dict_stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }

    return jsonify(dict_stats)
