#!/usr/bin/python3
"""Index Module"""

from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from api.v1.views import app_views
from flask import Flask, jsonify

from models import storage

@app_views.route('/status')
def status():
    """Return status OK"""
    return jsonify({"status": "OK"}), 200


@app_views.route('/stats')
def endpoint():
    """Endpoint that retrieves the number of each object"""
    count = {
        "amenities": storage.count(State),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return jsonify(count), 200
