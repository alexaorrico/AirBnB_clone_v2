#!/usr/bin/python3
"""
create a route /status on the object app_views that returns a JSON
and an endpoint that retrieves the number of each objects by type
"""

from flask import Flask, Blueprint, jsonify, request
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """function that returns the status"""
    if request.method == "GET":
    return jsonify({"status": "OK"})

@app_views.route('/status', methods=['GET'])
def get_stats():
    """function that returns count of all class objects"""
    if request.method == 'GET':
        response = {}
        texthbnb = {
            'Amenity': 'amenities',
            'City': 'cities',
            'Place': 'places',
            'Review': 'reviews',
            'State': 'states',
            'User': 'users'
        }
        for key, value in texthbnb.items():
            response[value] = storage.count(key)
        return jsonify(response)
