#!/usr/bin/python3
"""end point that retrieves the number of elements by type"""

from flask import Flask
from flask import jsonify
from models import storage
from api.v1.views import app_views


@app_views.route("/status")
def get_status():
    """ Shows the HTTP status 200 ok"""
    return jsonify({"status": "OK"}), 200

@app_views.route("/stats")
def get_count():
    """To get the number of any object, based on the type"""
    stats = {
        "Amenity": "amenity",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
        "User": "user"
    }
    result = {name: storage.count(cls) for cls, name in stats.items()}
    return jsonify(result)
