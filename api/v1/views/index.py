#!/usr/bin/python3
"""Blueprint"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.user import User
from models.state import State
from models.review import Review
from models.place import Place
from models.city import City
from models.amenity import Amenity


@app_views.route("/status", methods=['GET'])
def status():
    """status OK, when a GET is requested"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def _count():
    """Endpoint with the number of each object by type"""
    res = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return jsonify(res)
