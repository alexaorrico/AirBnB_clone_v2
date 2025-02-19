#!/usr/bin/python3
"""
API version 1 views
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def get_status():
    """send status of the server as JSON"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def get_stats():
    """send the number of each objects by type:
    """
    from models.engine.file_storage import classes
    tmp_dict = tmp_dict = {
            "amenities": "Amenity",
            "cities": "City",
            "places": "Place",
            "reviews": "Review",
            "states": "State",
            "users": "User"
            }
    tmp = {k: storage.count(classes.get(v)) for k, v in tmp_dict.items()}
    return jsonify(tmp)
