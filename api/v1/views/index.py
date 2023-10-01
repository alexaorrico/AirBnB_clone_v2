#!/usr/bin/python3
"""
This module defines a route status for a Flask application.

The route /status is defined on the Flask application instance app_views.
When a GET request is sent to /status, the status function is executed.
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'])
def status():
    """
    Return the server status as JSON.

    When this function is called, it returns a JSON response with a single
    key-value pair. The key is "status" and the value is "OK".
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """
    Retrieves the number of each objects by type
    Return the server status as JSON.

    When this function is called, it returns a JSON response with a multiple
    key-value pairs of objects by type.
    """
    classes = {"amenities": Amenity, "cities": City, "places": Place,
               "reviews": Review, "states": State, "users": User}
    counts = {}
    for key, cls in classes.items():
        counts[key] = storage.count(cls)
    return jsonify(counts)
