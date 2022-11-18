#!/usr/bin/python3
"""Index for the API"""
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from models import storage


items = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"
}


@app_views.route('/status', strict_slashes=False)
def ret_status():
    """funct that returns status ok"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def ret_stats():
    """return stadistics"""
    dicti = {}
    for key, value in items.items():
        dicti[key] = storage.count(value)
    return jsonify(dicti)
