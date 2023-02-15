#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from api.v1.views import app_views
from flask import jsonify
import models


@app_views.route('/status', methods=['GET'])
def status():
    """Returns status in JSON Format"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """Retrieves number of objects by type"""
    classes = {"amenities": "Amenity",
               "cities": "City",
               "places": "Place",
               "reviews": "Review",
               "states": "State",
               "users": "User"}
    count_dict = dict()
    for key, value in classes.items():
        count_dict[key] = models.storage.count(value)
    return jsonify(count_dict)
