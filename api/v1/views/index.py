#!/usr/bin/python3
"""eturns a JSON response
indicating the status is "OK".
"""
from flask import jsonify
from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """Check the status of the route"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def object_status():
    """Create an endpoint that retrieves the number of each object by type"""
    objects = {
        "amenities": 'Amenity',
        "cities": 'City',
        "places": 'Place',
        "reviews": 'Review',
        "states": 'State',
        "users": 'User'
    }
    object_counts = {
        key: storage.count(value)for key, value in objects.items()
        }
    return jsonify(object_counts)

