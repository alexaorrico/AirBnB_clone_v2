#!/usr/bin/python3
"""
Blueprint for index
"""

from api.v1.views import app_views
from flask import jsonify, Blueprint
from models import storage

from models.state import State
from models.amenity import Amenity
from models.review import Review
from models.place import Place
from models.user import User
from models.city import City


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """
    json object with app status as return
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """
    Retrieves the number of each object type
    """
    objects = {"amenities": 'Amenity', "cities": 'City', "places": 'Place',
               "reviews": 'Review', "states": 'State', "users": 'User'}

    objects = {key: storage.count(value) for key, value in objects.items()}

    return jsonify(objects)
