#!/usr/bin/python3
"""Index for our web flask"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', strict_slashes=False)
def status():
    """
    Return json status of web flask
    """
    bob = {'status': 'OK'}
    return jsonify(bob)


@app_views.route('/stats', strict_slashes=False)
def stats():
    """ Returns json of stats of number of objs """
    result = {"ammenities": storage.count(Amenity),
              "cities": storage.count(City), "places": storage.count(Place),
              "reviews": storage.count(Review), "states": storage.count(State),
              "users": storage.count(User)}
    return jsonify(result)
