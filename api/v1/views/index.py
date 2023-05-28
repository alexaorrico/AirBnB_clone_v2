#!/usr/bin/python3
""" creates a route for the status """
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status", strict_slashes=False)
def status():
    """ Register the route """
    
    status = {'status': 'OK'}
    return jsonify(status)

@app_views.route("/stats", strict_slashes=False)
def get_stats():
    """ return the stats of objects """

    models = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User"
    }
    stats_dict = {
        att: storage.count(cls)
        for att, cls in models.items()
    }

    return jsonify(stats_dict)
