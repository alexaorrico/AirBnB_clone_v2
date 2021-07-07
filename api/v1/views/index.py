#!/usr/bin/python3
"""Module with routes for app_views blueprint"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"amenities": "Amenity", "cities": "City", "places": "Place",
           "reviews": "Review", "states": "State", "users": "User"}


@app_views.route('/status')
def status():
    """Returns a json with status ok"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def count_obj():
    """Retrieves the number of each objects by type"""
    my_dict = {}
    for k, v in classes.items():
        my_dict[k] = storage.count(v)
    return jsonify(my_dict)
