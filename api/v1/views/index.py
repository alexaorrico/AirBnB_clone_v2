#!/usr/bin/python3
"""Module with a flask script"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

@app_views.route('/status')
def status():
    """Method that returns status ok"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """Method that returns the stats(number of objects)"""
    json_dict = {
            "amenities": storage.count(Amenity), 
            "cities": storage.count(City),
            "places": storage.count(Place),
            "reviews": storage.count(Review),
            "states": storage.count(State),
            "users": storage.count(User)
            }
    return jsonify(json_dict)
