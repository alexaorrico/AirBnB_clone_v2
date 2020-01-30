#!/usr/bin/python3
""" doc for index.py """
from flask import jsonify
from models import storage
from api.v1.views import app_views

@app_views.route('/status')
def status():
    """ doc for status method """
    return jsonify({"status": "OK"})

@app_views.route('/stats')
def stats():
    """ doc for stats """
    list_counts = {"amenities": storage.count("Amenity"), 
                   "cities": storage.count("City"),
                   "places": storage.count("Place"),
                   "reviews": storage.count("Review"),
                   "states": storage.count("State"),
                   "users": storage.count("User")}
    return jsonify(list_counts)
