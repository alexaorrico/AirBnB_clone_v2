#!/usr/bin/python3
"""Status of your API"""

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage


@app_views.route("/status")
def status():
    """returns a JSON"""
    return jsonify({"status": "OK" })


@app_views.route("/stats")
def stats():
    """retrieves the number of each objects by type"""
    stat = {
    "amenities": storage.count("Amenity"), 
    "cities": storage.count("City"), 
    "places": storage.count("Place"), 
    "reviews": storage.count("Review"), 
    "states": storage.count("State"), 
    "users": storage.count("User")
    }

    return jsonify(stat)
