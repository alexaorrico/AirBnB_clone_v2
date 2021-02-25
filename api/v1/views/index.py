#!/usr/bin/python3
"""Our first API"""


from flask import Flask
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
    """Route on the object app_views that returns a JSON"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def count_objstype():
    """count each objects by type"""
    list_objs = {
        'amenities': storage.count(Amenity),
        'cities': storage.count(City),
        'places': storage.count(Place),
        'reviews': storage.count(Review),
        'states': storage.count(State),
        'users': storage.count(User), }
    return jsonify(list_objs)
