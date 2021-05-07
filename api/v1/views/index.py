#!/usr/bin/python3
""" Index """
from api.v1.views import app_views
import flask
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """ return json """
    return flask.jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'])
def stats():
    """
    Endpoint that retrieves the number of each objects by type
    """
    stats = {
            "amenities": "Amenity",
            "cities": "City",
            "places": "Place",
            "reviews": "Review",
            "states": "State",
            "users": "User"
            }
    new = {}
    for key, value in stats.items():
        new[key] = storage.count(value)

    return flask.jsonify(new)
