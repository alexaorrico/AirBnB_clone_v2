#!/usr/bin/python3
"""this module has route /status
"""
from models import storage
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from flask import Flask, jsonify
from api.v1.views import app_views


amenities_ = storage.count(Amenity)
cities_ = storage.count(City)
places_ = storage.count(Place)
reviews_ = storage.count(Review)
states_ = storage.count(State)
users_ = storage.count(User)


data = {"amenities": amenities_,
        "cities": cities_,
        "places": places_,
        "reviews": reviews_,
        "states": states_,
        "users": users_
        }


@app_views.route('/status', strict_slashes=False)
def return_json():
    """return a JSON: 'status': 'OK'"""
    status = {"status": "OK"}
    return jsonify(status)


@app_views.route('/stats', strict_slashes=False)
def obj_no():
    """retrieves the number of each objects by type"""
    return jsonify(data)
