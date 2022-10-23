#!/usr/bin/python3
"""Module app.py: starts the flask app"""
from api.v1.views import app_views
from flask import jsonify
from models import storage

dictionary = {
    'amenities': 'Amenity',
    'cities': 'City',
    'places': 'Place',
    'reviews': 'Review',
    'states': 'State',
    'users': 'User',
}


@app_views.route("/status")
def status():
    """returns the status"""
    return jsonify(status='OK')


@app_views.route("/stats")
def stats():
    """returns the statistics of each class"""
    new_dict = {k: storage.count(v) for (k, v)
                in dictionary.items()}
    return jsonify(new_dict)
