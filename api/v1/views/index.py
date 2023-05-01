#!/usr/bin/python3
"""
This module contains the routes for the web application
"""
from flask import jsonify
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage
from models.city import City
from models.state import State
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """status of API"""
    return jsonify({'status': "OK"})


@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def number_of_objects():
    """retrieves the number of each objects by type"""
    objs = {
        'amenities': storage.count(Amenity),
        'cities': storage.count(City),
        'places': storage.count(Place),
        'reviews': storage.count(Review),
        'states': storage.count(State),
        'users': storage.count(User)
    }

    return jsonify(objs)
