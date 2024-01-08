#!/usr/bin/python3
'''
    flask containing general routes
    routes:
        /status:    displays"status":"OK"
        /stats:     displays total for all classes
'''
from flask import jsonify
from api.v1.views import app_views
from models import storage

@app_views.route('/api/v1/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """Retrieve the number of each object by type"""
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
    }
    return jsonify(stats)
