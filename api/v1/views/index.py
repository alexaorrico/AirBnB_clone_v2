#!/usr/bin/env python3

"""Define a route /status on the object app_views that
   returns a json
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Return a json object"""
    return jsonify({
        "status": "OK"
    })


@app_views.route('/stats')
def stats():
    amenity_count = storage.count("Amenity")
    city_count = storage.count("City")
    place_count = storage.count("Place")
    review_count = storage.count("Review")
    state_count = storage.count("State")
    user_count = storage.count("User")

    return jsonify({
        "amenities": amenity_count,
        "cities": city_count,
        "places": place_count,
        "reviews": review_count,
        "states": state_count,
        "users": user_count
    })
