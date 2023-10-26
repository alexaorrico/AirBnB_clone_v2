#!/usr/bin/python3
""" Returns JSON."""

from flask import jsonify
from models import storage
from api.v1.views import app_views, Amenity, City, Place, Review, State, User


@app_views.route('/status', strict_slashes=False, methods=['GET'])
def status():
    """ Returns the status."""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False, methods=['GET'])
def stats():
    """ Retrieves the number of each objects by type."""
    counts = {
            "amenities": storage.count(Amenity),
            "cities": storage.count(City),
            "places": storage.count(Place),
            "reviews": storage.count(Review),
            "states": storage.count(State),
            "users": storage.count(User)
            }
    return jsonify(counts)
