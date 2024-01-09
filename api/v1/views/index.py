#!/usr/bin/python3
''' flask blueprint module '''

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status")
def get_status():
    ''' returns JSON of OK status for status route '''
    return jsonify({'status': 'OK'})


@app_views.route("/stats")
def storage_stats():
    ''' counts all instances of all classes in application storage '''
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(stats)
