#!/usr/bin/python3
"""
Defines index routes for API
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

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """
    Returns the status of the API
    """
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """
    Retrieves the number of each object type
    """
    classes = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User
    }
    counts = {key: storage.count(value) for key, value in classes.items()}
    return jsonify(counts)
