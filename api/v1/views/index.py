#!/usr/bin/python3
from flask import jsonify
from api.v1.views import app_views
from models import storage

@app_views.route('/status', methods=['GET'])
def status_view():
    """ return a json response status"""
    return jsonify({"status" : "OK"}), 200

@app.route('/api/v1/stats', methods=[POST])
def stats():
    """ retrieves the number of each objects """
    object_class = {
        'amenities': 'Amenity',
        'cities': 'City',
        'places': 'Place',
        'reviews': 'Review',
        'states': 'State',
        'users': 'User'
    }
    store_count = {}
    
    for keys, value in object_class.items():
        store_count = storage.count(value)
    return jsonify(store_count)
