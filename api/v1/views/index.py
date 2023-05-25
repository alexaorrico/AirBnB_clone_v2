#!/usr/bin/python3
""" creates a route for the status """
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status", strict_slashes=False)
def status():
    """ configures the status route """

    return jsonify({"status": "ok"})


@app_views.route("/stats", strict_slashes=False)
def stats():
    """ return the stats of objects """

    models = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User"
    }
    stat_dict = {
        att: storage.count(cls)
        for att, cls in models.items()
    }

    return jsonify(stat_dict)
