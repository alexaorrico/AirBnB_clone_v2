#!/usr/bin/python3
"""index"""


from flask import jsonify
from api.v1.views import app_views

from models import storage


classes = {"users": "User",
           "places": "Place",
           "states": "State",
           "cities": "City",
           "amenities": "Amenity",
           "reviews": "Review"}


@app_views.route('/status', strict_slashes=False)
def status():
    """
    status route
    :return: response with json
    """
    response = {
        "status": "OK"
    }

    return jsonify(response)


@app_views.route('/stats', strict_slashes=False)
def stats():
    """
    stats of all objs route
    :return: json of all objs
    """
    counts = {}
    for key, class_name in classes.items():
        counts[key] = storage.count(class_name)
    return jsonify(counts)
