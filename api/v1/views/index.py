#!/usr/bin/python3

"""View for index that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import  State


@app_views('/status')
def get_status():
    """Check status of route"""
    return jsonify({'status': 'OK'})


@app_views('/stats')
def get_stats():
    """Retrieves the number of each objects by type"""
    objects = {"amenities": 'Amenity', "cities": 'City', 
               "places": 'Place', "reviews": 'Review',
               "states": 'State', "users": 'User'}

    for key, value in objects.items():
        objects[key] = storage.count(value)
    return jsonify(objects)
