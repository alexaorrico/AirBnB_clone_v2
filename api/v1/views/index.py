#!/usr/bin/python3
"""
index.py

This module serves as the entry point for the Flask application.
It imports the necessary modules and classes,
configures the Flask application, and sets up the routes for the API endpoints.

Classes:
    None

Functions:
    route():
        Returns an OK status code in JSON format.

    stats():
        Retrieves the number of each object by type.

Routes:
    /status:
        GET: Returns an OK status code in JSON format.

    /stats:
        GET: Retrieves the number of each object by type.

Dependencies:
    - Flask
    - api.v1.views
    - models
    - models.amenity
    - models.city
    - models.place
    - models.review
    - models.state
    - models.user

"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


classes = {
    "amenities": storage.count(Amenity),
    "cities": storage.count(City),
    "places": storage.count(Place),
    "reviews": storage.count(Review),
    "states": storage.count(State),
    "users": storage.count(User)
}


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def route():
    """Returns an OK status code in json format"""
    response = {
        "status": "OK"
    }

    return jsonify(response), 200


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """Retrieves the number of each objects by type"""
    stats_dict = {}
    for key, value in classes.items():
        stats_dict[key] = value

    return jsonify(stats_dict)
