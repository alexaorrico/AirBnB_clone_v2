#!/usr/bin/python3
"""
Index view
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """Return status of API"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """Return number of objects by type"""
    from models import storage
    classes = {"amenities": "Amenity", "cities": "City", "places": "Place",
               "reviews": "Review", "states": "State", "users": "User"}
    return jsonify(
            {key: storage.count(value) for key, value in classes.items()}
            )
