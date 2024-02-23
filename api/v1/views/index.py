#!/usr/bin/python3
'''Module containing instructions for the flask blueprint app_views'''
from api.v1.views import app_views
from flask import jsonify
from models import storage
from api import mapped_classes


@app_views.route('/status', strict_slashes=False, methods=['GET'])
def status():
    '''Returns a JSON STATUS OK'''
    return jsonify({'status': 'OK'})


@app_views.route('/stats', strict_slashes=False, methods=['GET'])
def count_objects():
    '''Returns the jsonified version of each counted object'''
    return jsonify({
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    })
