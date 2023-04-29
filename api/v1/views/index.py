#!/usr/bin/python3
""" Index File """

from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """ Returns Status of a """
    return jsonify({
        "status": "OK"
        })
    status = {"status": "OK"}
    return jsonify(status)


@app_views.route('/stats', strict_slashes=False)
def class_number():
    """Returns The Number of Each Individual Class"""
    dict_count = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "Places": storage.count(Place),
        "Review": storage.count(Review),
        "state": storage.count(State),
        "users": storage.count(User)
    }
    return jsonify(dict_count)
