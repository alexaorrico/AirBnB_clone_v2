#!/usr/bin/python3
"""
start api
"""
from flask import jsonify
from models import storage
from . import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status", methods=['GET'])
def status():
    """ return status of object """
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=['GET'])
def number_of_objects():
    """ Retrieves the number of each object type. """
    stats_dict = {
        'amenities': storage.count(Amenity),
        'cities': storage.count(City),
        'places': storage.count(Place),
        'reviews': storage.count(Review),
        'states': storage.count(State),
        'users': storage.count(User),
    }
    return jsonify(stats_dict)
