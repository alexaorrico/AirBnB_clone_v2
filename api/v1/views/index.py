#!/usr/bin/python3
"""
index
"""
from flask import jsonify, Blueprint
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """ checking the status of route """
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def number_of_objects():
    """ Retrieves the number of each objects by type """
    objects = {"amenities": 'Amenity', "cities": 'City', "places": 'Place',
               "reviews": 'Review', "states": 'State', "users": 'User'}
    for key, value in objects.items():
        objects[key] = storage.count(value)
    return jsonify(objects)
