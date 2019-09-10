#!/usr/bin/python3
"""function to create the route status"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """status render template for json"""
    return jsonify({"status": "OK"})


@app_views.app_errorhandler(404)
def handle_404(err):
    """status render template for json"""
    return jsonify({"error": "Not found"}), 404


@app_views.route('/stats')
def stats():
    """status render template for json"""
    dict_objs = {'amenities': 'Amenity', 'cities': 'City', 'places': 'Place',
                 'reviews': 'Review', 'states': 'State', 'users': 'User'}
    new_dict = {}
    for k, v in dict_objs.items():
        new_dict[k] = storage.count(v)
    return jsonify(new_dict)
