#!/usr/bin/python3
"""
Craeted index view with /status route on object app_view
"""


from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def get_status():
    """Gets the status of the API."""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def get_stats():
    """ retrieves the number of each objects by type"""

    Obj_count = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User
    }

    for key, value in Obj_count.items():
        Obj_count[key] = storage.count(value)
    return jsonify(Obj_count)
