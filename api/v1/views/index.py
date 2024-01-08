#!/usr/bin/python3
'''
    flask application with routes
    routes:
        /status:    display "status":"OK"
        /stats:     dispaly total for all classes
'''
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status")
def status():
    '''
        returns JSON of OK status
    '''
    return jsonify({'status': 'OK'})


@app_views.route("/stats")
def storage_stats():
    '''
        counts all instances of all classes in storage
    '''
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(stats)
