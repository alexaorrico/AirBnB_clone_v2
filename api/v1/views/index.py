#!/usr/bin/python3
"""
script that starts a Flask web application:
"""

from api.v1.views import app_views
from flask import jsonify, Flask, Response
from models import storage
from werkzeug.wrappers import response

all_class = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"
}


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
    resp = {}
    for key, value in all_class.items():
        resp[key] = storage.count(value)
    return jsonify(resp)
