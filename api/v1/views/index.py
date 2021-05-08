#!/usr/bin/python3
""" Index to api"""
from api.v1.views import app_views
import flask
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """ return json """
    return flask.jsonify({'status': 'OK'})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """
    Endpoint that retrieves the number of each objects by type
    """
    statsc = {
            "amenities": "Amenity",
            "cities": "City",
            "places": "Place",
            "reviews": "Review",
            "states": "State",
            "users": "User"
            }
    for key, value in statsc.items():
        statsc[key] = storage.count(value)

    return flask.jsonify(statsc)
