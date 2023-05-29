#!/usr/bin/python3
""""""

from flask import jsonify
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route('/status')
def index():
    data = {
        "status": "OK"
    }
    return jsonify(data)


@app_views.route('/stats')
def stats():
    users = len(storage.all(User).values())
    amenities = len(storage.all(Amenity).values())
    states = len(storage.all(State).values())
    places = len(storage.all(Place).values())
    reviews = len(storage.all(Review).values())
    cities = len(storage.all(City).values())

    data = {
        "amenities": amenities,
        "cities": cities,
        "places": places,
        "reviews": reviews,
        "states": states,
        "users": users,
    }

    return jsonify(data)
