#!/usr/bin/python3
"""index page"""
from api.v1.views import app_views
from flask import jsonify
from models import storage, Amenity, City, Place, Review, State, User


@app_views.route("/status", strict_slashes=False)
def status():
    """return: status ok"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def cls_obj_count():
    """retrieves the number of each objects by type"""
    data = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }

    return jsonify(data)
