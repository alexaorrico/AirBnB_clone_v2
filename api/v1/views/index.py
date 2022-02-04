#!/usr/bin/python3
"""Module view for index"""
from flask import jsonify
from models import storage
from api.v1.views import app_views


@app_views.route('/status')
def get_tasks():
    """Return the JSON status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def count_function():
    """retrieves the number of each objects by type"""
    count_dict = {}
    count_dict["amenities"] = storage.count('Amenity')
    count_dict["cities"] = storage.count('City')
    count_dict["places"] = storage.count('Place')
    count_dict["reviews"] = storage.count('Review')
    count_dict["states"] = storage.count('State')
    count_dict["users"] = storage.count('User')
    return jsonify(count_dict)
