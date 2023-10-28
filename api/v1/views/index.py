#!/usr/bin/python3
"""A route that will display the status code"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    objs = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "place": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return jsonify(objs)
