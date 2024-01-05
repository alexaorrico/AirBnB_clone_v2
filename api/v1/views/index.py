#!/usr/bin/python3
"""API Routes"""
from flask import jsonify
from models import storage

from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', strict_slashes=False)
def api_status_view():
    """return the API status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats_view():
    """Count objects"""
    return jsonify({
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    })
