#!/usr/bin/python3
""" index views """
from api.v1.views import app_views
from flask import jsonify
from models import State
from models import Place
from models import storage
from models import User
from models import Review
from models import City
from models import Amenity


@app_views.route('/status', strict_slashes=False)
def status():
    return jsonify({'status': 'OK'})


@app_views.route('/stats', strict_slashes=False)
def stats():
    data = {
            "amenities": storage.count(Amenity),
            "cities": storage.count(City),
            "places": storage.count(Place),
            "reviews": storage.count(Review),
            "states": storage.count(State),
            "users": storage.count(User)
            }
    return jsonify(data)
