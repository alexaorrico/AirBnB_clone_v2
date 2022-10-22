#!/usr/bin/python3
"""Index file"""

from flask import jsonify
from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', methods=['GET'])
def states():
    """Returns states in storage"""
    states_dict = [x.to_dict() for x in storage.all(State)]
    return jsonify(states_dict)

@app_views.route('/stats', methods=['GET'])
def stat():
    """Returns statistics of objects"""
    sts_dict = {
                "amenities": storage.count(Amenity), 
                "cities": storage.count(City), 
                "places": storage.count(Place), 
                "reviews": storage.count(Review), 
                "states": storage.count(State), 
                "users": storage.count(User)
                }
    return jsonify(sts_dict)