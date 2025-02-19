#!/usr/bin/python3
"""Defining the routes"""

from api.v1.views import app_views
from flask import jsonify, make_response
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Returns JSON """
    return jsonify(status="OK")


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """
    Create an endpoint that retrieves the number of each objects by type
    """
    return jsonify({
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "states": storage.count(State),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "users": storage.count(User)
        })
