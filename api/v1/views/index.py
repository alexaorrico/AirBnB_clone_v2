#!/usr/bin/python3
"""
flask application module
"""

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def jsonStatus():
    """ returns a JSON: "status": "OK" """
    return jsonify(status=' ok')


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """ retrieves number of objects by type """
    classes = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User"
    }

    for key, dbObject in classes.items():
        classes[key] = storage.count(dbObject)
    return jsonify(classes)
