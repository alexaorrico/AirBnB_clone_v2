#!/usr/bin/python3
"""variable app_views which is an instance of Blueprint"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """status api"""
    new_dict = {}
    new_dict['status'] = "OK"
    return jsonify(new_dict)


@app_views.route('/stats')
def stats():
    """number of each objects by type"""
    objs_count = {}
    objs_count['amenities'] = storage.count("Amenity")
    objs_count['cities'] = storage.count("City")
    objs_count['places'] = storage.count("Place")
    objs_count['reviews'] = storage.count("Review")
    objs_count['states'] = storage.count("State")
    objs_count['users'] = storage.count("User")
    return jsonify(objs_count)
