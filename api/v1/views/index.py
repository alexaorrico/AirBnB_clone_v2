#!/usr/bin/python3
''' Index file '''
from api.v1.views import app_views
from models import storage
from flask import jsonify


classes = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"
}


@app_views.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    '''return object stats'''
    stat_count = {}
    for key, value in classes.items():
        stat_count[key] = storage.count(value)

    return jsonify(stat_count)
