#!/usr/bin/python3
"""index file, main view file
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def service_status():
    """returns the status of the RESTful service"""
    """ TODO check if this formatting is okay for json response with
        holberton checker """
    return jsonify({'status': 'OK'})


@app_views.route('/stats', strict_slashes=False)
def object_stats():
    """returns the count of object types"""

    classes = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User"
        }
    for k, v in classes.items():
        classes[k] = storage.count(v)
    return jsonify(classes)
