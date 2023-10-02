#!/usr/bin/python3
"""Returns a Json response"""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models import amenity, city, place, review, state, user


@app_views.route('/status')
def status_check():
    '''Returns status code'''
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def object_stats():
    """Retrieves the no of each object by type"""
    objects = {
            "amenities": storage.count(amenity.Amenity),
            "cities": storage.count(city.City),
            "places": storage.count(place.Place),
            "reviews": storage.count(review.Review),
            "states": storage.count(state.State),
            "users": storage.count(user.User),
            }
    return jsonify(objects)
