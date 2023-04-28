#!/usr/bin/python3
"""This file contains the definition of API routes v1"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns a JSON object indicating the state of the API"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """Retrieves the number of each object type"""
    obj_counts = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return jsonify(obj_counts)
