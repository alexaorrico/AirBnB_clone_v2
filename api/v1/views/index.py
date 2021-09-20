#!/usr/bin/python3
"""
Views' index file
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from models.amenity import Amenity


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def jsonify_app():
    """ Function that returns a JSON """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def some_stats():
    """ Retrieves the number of each objects by type """
    dict = {"amenities": storage.count(Amenity),
            "cities": storage.count(City),
            "places": storage.count(Place),
            "reviews": storage.count(Review),
            "states": storage.count(State),
            "users": storage.count(User)}
    return jsonify(dict)
