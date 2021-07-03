#!/usr/bin/python3
""" prepares data for easier viewing """

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    """ health checker """
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats_count():
    """ counts stuff """
    retval = {
        "amenities": storage.count('Amenity'),
        "cities": storage.count('City'),
        "places": storage.count('Place'),
        "reviews": storage.count('Review'),
        "states": storage.count('State'),
        "users": storage.count('User'),
    }
    return jsonify(retval)
