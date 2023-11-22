#!/usr/bin/python3
""" index for RESTful API """
# Michael edited 11/20 10:50 AM full checks

from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    """ Status of API """
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    """ Stats of API """

    from models import storage

    classes = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User"
    }
    return jsonify({key: storage.count(val) for key, val in classes.items()})
