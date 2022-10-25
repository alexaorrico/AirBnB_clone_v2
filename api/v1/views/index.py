#!/usr/bin/python3
""" show status and stats """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """ return a 200 status for the status route """
    app_views = {'status': 'OK'}
    return jsonify(app_views), 200


@app_views.route('/stats', strict_slashes=False)
def stats():
    """ return the count of all members in the database """
    stat_dict = {
            "amenities": storage.count("Amenity"),
            "cities": storage.count("City"),
            "places": storage.count("Place"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("User")
            }
    return jsonify(stat_dict)
