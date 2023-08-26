#!/usr/bin/python3
"""Module that have the route of app_views"""
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
def hbnbstatus():
    """function that return json on status route"""
    return jsonify({'status': "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats_hbnb():
    """function: retrieves a dictionary with the amount of objects"""
    obj_in_class = [Amenity, City, Place, Review, State, User]
    names = ["amenities", "cities", "places", "reviews", 'states', 'users']

    obj_amount = {}
    for amount in range(len(obj_in_class)):
        obj_amount[names[amount]] = storage.count(obj_in_class[amount])

    return jsonify(obj_amount)
