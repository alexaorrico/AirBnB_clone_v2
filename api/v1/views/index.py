#!/usr/bin/python3

from api.v1.views import app_views
from models import storage
from flask import jsonify


@app_views.route('/status')
def status():
    """ aplication status """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """ counts all classes """
    classes = {"users": 'User', "states": 'State', "amenities": 'Amenity',
               "cities": 'City', "places": 'Place', "reviews": 'Review'}
    json = {}
    for key, value in classes.items():
        json[key] = storage.count(value)
    return jsonify(json)
