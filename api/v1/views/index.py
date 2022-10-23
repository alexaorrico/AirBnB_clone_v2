#!/usr/bin/python3
""" index module showing the status endpoint """
import json
from models import storage
from models.state import State
from models.amenity import Amenity
from models.user import User
from models.city import City
from models.review import Review
from models.place import Place

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def show_status():
    return jsonify({"status": "OK"})


@app_views.route('/api/v1/stats')
def show_count():
    new_dict = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return jsonify(new_dict)
