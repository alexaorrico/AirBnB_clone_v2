#!/usr/bin/python3
""" index file """

from flask import jsonify
from api.v1.views import app_views
from models.state import State
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """ test status OK """
    return jsonify({"status": "OK"})


@app_views.route("/api/v1/stats", methods=['GET'], strict_slashes=False)
def stats():
    """ return the count of all objects"""
    aminities = storage.count(Amenity)
    cities = storage.count(City)
    places = storage.count(Place)
    reviews = storage.count(Review)
    states = storage.count(State)
    users = storage.count(User)
    return jsonify(
        {"amenities": aminities,
         "cities": cities,
         "places": places,
         "reviews": reviews,
         "states": states,
         "users": users}
    )
