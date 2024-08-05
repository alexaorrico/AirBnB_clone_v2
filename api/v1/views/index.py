#!/usr/bin/python3
"""
Module to provide JSON responses for API endpoints
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

classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route('/status', strict_slashes=False)
def index():
    """Return the status of the API"""
    response = {"status": "OK"}
    return jsonify(response)


@app_views.route('/stats', strict_slashes=False)
def stats():
    """Return the count of each object type"""
    response = {}
    for key, value in classes.items():
        response[key] = storage.count(value)
    return jsonify(response)
