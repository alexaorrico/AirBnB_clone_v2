#!/usr/bin/python3
"""
"""

from api.v1.views import app_views
from flask import jsonify
from models import *

@app_views.route("/status")
def status():
    return jsonify({"status": "OK"})

@app_views.route("/stats")
def num_of_objs():
    obj_count = {
            "amenities": storage.count(amenity.Amenity),
            "cities": storage.count(city.City),
            "places": storage.count(place.Place), 
            "reviews": storage.count(review.Review),
            "states": storage.count(state.State),
            "users": storage.count(user.User)
            }
    return jsonify(obj_count)

