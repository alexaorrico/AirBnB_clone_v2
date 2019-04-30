#!/usr/bin/python3
from models import storage
from flask import jsonify
from api.v1.views import app_views


@app_views.route("/", strict_slashes=False)
def index():
    """index route of app"""
    return "No entries here so far\n"


@app_views.route("/status", strict_slashes=False)
def status():
    """status method to return status to api request"""
    return jsonify(status="OK")


@app_views.route("/stats", strict_slashes=False)
def stats():
    """Stats route for flask app"""
    return jsonify(amenities=storage.count("Amenity"),
                   cities=storage.count("City"),
                   places=storage.count("Place"),
                   reviews=storage.count("Review"),
                   states=storage.count("State"),
                   users=storage.count("User"))
