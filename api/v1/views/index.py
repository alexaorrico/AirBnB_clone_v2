#!/usr/bin/python3
"""
creates the route
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """
    Gets the status of the API and returns it
    """
    return jsonify(status="OK")


@app_views.route('/stats', methods=['GET'])
def count():
    """
    Counts the number of each object
    """

    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")}
                    )
