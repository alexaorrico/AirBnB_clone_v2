#!/usr/bin/python3
""" index file """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """ Return http status response """
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def get_stats():
    """ retive the number of each obj by type """
    new_dict = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states":  storage.count("State"),
        "users":  storage.count("User")
    }
    return jsonify(new_dict)
