#!/usr/bin/python3
"""index.py to connect to API"""
from api.v1.views import app_views
from flask import jsonify

from models import storage
from models.state import State
from models.amenity import Amenity
from models.user import User
from models.city import City
from models.review import Review
from models.place import Place


@app_views.route('/status', strict_slashes=False)
def hbnbStatus():
    """hbnbStatus"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def hbnbStats():
    """hbnbStats"""
    new_dict = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return jsonify(new_dict)
