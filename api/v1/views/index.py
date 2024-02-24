#!/usr/bin/python3

"""
Returns a JSON
"""
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify

@app_views.route('/status', methods=['GET'])
def get_status():
    """A route that returns a JSON"""
    return jsonify({"status": "OK"})

stats_blueprint = Blueprint('stats', __name__, url_prefix='/api/v1')


@stats_blueprint.route('/stats', methods=['GET'])
def get_stats():
    # Retrieve counts of each object type
    counts = {
        'amenities': storage.count('Amenities'),
        'cities': storage.count('Cities'),
        'places': storage.count('Places'),
        'reviews': storage.count('Reviews'),
        'states': storage.count('States'),
        'users' : storage.count('Users'),
    }
    return jsonify(counts), 200