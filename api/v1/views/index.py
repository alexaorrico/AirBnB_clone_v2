#!/usr/bin/python3
'''Define API view routes for status and stats endpoints.'''

from flask import jsonify
from api.v1.views import app_views
from models import storage


classes = {
    'amenities': 'Amenity',
    'cities': 'City',
    'places': 'Place',
    'reviews': 'Review',
    'states': 'State',
    'users': 'User'
}


@app_views.route('/status', methods=['GET'])
def status():
    '''Returns a JSON response with the status of the API.'''
    return jsonify(status='OK')


@app_views.route('/stats', methods=['GET'])
def stats():
    '''Returns the count of each object by type.'''
    counts = {
        cls: storage.count(cls_name)
        for cls, cls_name in classes.items()
        }
    return jsonify(counts)
