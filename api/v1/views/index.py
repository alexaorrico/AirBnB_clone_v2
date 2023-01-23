#!/usr/bin/python3
"""
Creates the Status route for app_views
"""

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def status_ok():
    """ returns  json message with status OK"""
    return jsonify({"status": "OK"}), 200


@app_views.route('/stats', methods=['GET'])
def obj_num():
    """ retrieves number of objects by type"""
    objects = {
        "amenities": storage.count('Amenity'),
        "cities": storage.count('City'),
        "places": storage.count('Place'),
        "reviews": storage.count('Review'),
        "states": storage.count('State'),
        "users": storage.count('User')
    }

    return jsonify(objects), 200
