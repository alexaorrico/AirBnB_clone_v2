#!/usr/bin/python3
"""
Route Index
"""

from api.v1.views import app_views, Place, City, Amenity, Review, State, User
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False, methods=['GET'])
def status():
    """Return API status"""
    return jsonify({"status": "OK"}), 200


@app_views.route('/stats', strict_slashes=False, methods=['GET'])
def stats():
    """Return API stats of objects"""
    stats = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return jsonify(stats), 200
