#!/usr/bin/python3
'''
    Flask application with general routes.

    Routes:
        - /status: Display {"status": "OK"}
        - /stats: Display total counts for all classes in storage.
'''

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    '''
    Endpoint to return JSON indicating the status is "OK".

    Returns:
        JSON: {"status": "OK"}
    '''
    return jsonify({'status': 'OK'})


@app_views.route("/stats")
def storage_counts():
    '''
    Endpoint to return counts of all classes in storage.

    Returns:
        JSON: Counts of all classes in storage.
    '''
    class_counts = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(class_counts)
