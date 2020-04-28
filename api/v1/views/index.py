#!/usr/bin/python3
""" creates a route """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    """ Returns /status response"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    """ Returns the stats """
    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")})
