#!/usr/bin/python3
"""This module defines a route for stats"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.city import City
from models.review import Review
from models.user import User


@app_views.route('/status')
def status():
    """Return a JSON with status: OK"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """Retrieve the number of each object by type"""
    stats = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return jsonify(stats)
