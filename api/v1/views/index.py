#!/usr/bin/python3
"""index.py"""
from flask import jsonify
from api.v1.views import app_views
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.user import User
from models import storage


@app_views.route("/status")
def hbnb_status():
    """ return the status of the api """
    return jsonify({"status": "OK"}), 200


@app_views.route("/stats")
def hbnb_stats():
    """ return in a json format the stats
    showing the number of objects in db """

    stats = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }

    return jsonify(stats), 200
