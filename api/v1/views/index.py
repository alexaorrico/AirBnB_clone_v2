#!/usr/bin/python3
"""has the routes to be used"""
from api.v1.views import app_views
from flask import jsonify
import json
from models import storage


@app_views.route('/status', methods=['GET'])
def get_status():
    response = {
            'status': 'OK'
            }
    formatted_json = json.dumps(response, indent=2)
    print(formatted_json)
    return jsonify(response)


@app_views.route('/stats', methods=['GET'])
def get_stats():
    """retrieves the number of each objects by type"""
    stat = {
            'amenities': storage.count('Amenity'),
            'cities': storage.count('City'),
            'places': storage.count('Place'),
            'reviews': storage.count('Review'),
            'states': storage.count('State'),
            'users': storage.count('User')
            }
    return jsonify(stat)
