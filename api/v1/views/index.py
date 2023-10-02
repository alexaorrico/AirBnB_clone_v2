#!/usr/bin/python3
"""api status"""

from flask import jsonify
from api.v1.views import app_views
from models import storage

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def api_status():
    """Return the status of your API"""
    return jsonify({"status": "OK"})

@app_views.route('/api/v1/stats', methods=['GET'], strict_slashes=False)
def api_stats():
    """Retrieve the number of each object by type"""
    classes = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User),
    }
    return jsonify(classes)
