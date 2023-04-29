#!/usr/bin/python3
''' index and status view for the API'''
from flask import jsonify
from models import storage
from api.v1.views import app_views


@app_views.route('/status')
def get_api_status():
    '''Gets the status of the api
    '''
    # return jsonify(status='OK')
    return jsonify({'status': 'OK'})

@app_views.route('/stats')
def get_api_v1_stats():
    """gets the number of each objects"""

    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }

    return jsonify(stats)
