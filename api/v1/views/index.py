#!/usr/bin/python3
"""
Your first endpoint (route) will be to return the
status of your API:
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


@app_views.route('/status', strict_slashes=False)
def status_():
    """Initial status
    """
    stats = {
        "status": "OK"
        }
    return {
        "status": "OK"
    }


@app_views.route('/stats', strict_slashes=False)
def count_():
    """Count all
    """
    dict_json = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return jsonify(dict_json)
