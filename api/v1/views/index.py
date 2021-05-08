#!/usr/bin/python3
"""
Flask route that returns status of JSON object response in app_views
"""
from api.v1.views import app_views
from flask import Flask, jsonify, request
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """ Returns status message in JSON
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """ Returns stats message in JSON
    """
    if request.method == 'GET':
        amens = storage.count("Amenity")
        cities = storage.count("City")
        places = storage.count("Place")
        reviews = storage.count("Review")
        states = storage.count("State")
        users = storage.count("User")

    return ({"amenities": amens,
             "cities": cities,
             "places": places,
             "reviews": reviews,
             "states": states,
             "users": users})
