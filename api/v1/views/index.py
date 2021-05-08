#!/usr/bin/python3
""" Index to api to handle status and stats route"""
from api.v1.views import app_views
import flask
from models import storage


@app_views.route("/status", strict_slashes=False)
def return_status():
    """ Returns the status of the api. """
    status = {"status": "OK"}
    return(jsonify(status))


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
