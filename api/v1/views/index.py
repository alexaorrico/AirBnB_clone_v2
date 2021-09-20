#!/usr/bin/python3
"""
script that starts a Flask web application:
"""

from api.v1.views import app_views
from flask import jsonify, Flask, Response
from models import storage


@app_views.route('/status')
def status():
    """
    Status
    """
    status = {"status": "OK"}
    return jsonify(status)


@app_views.route("/stats")
def stats():
    """ retrieves the number of each objects by type
    """
    status = {"amenities": storage.count("Amenity"),
              "cities": storage.count("City"),
              "places": storage.count("Place"),
              "reviews": storage.count("Review"),
              "states": storage.count("State"),
              "users": storage.count("User")}
    return jsonify(status)
