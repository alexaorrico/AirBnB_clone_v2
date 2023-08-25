#!/usr/bin/python3
"""imports app_views. creates route for status"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """returns a json ok string
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """returns a json with number of objects in db categorized by type
    """
    tgts = {"amenities": "Amenity", "cities": "City", "places": "Place",
            "reviews": "Review", "states": "State", "users": "User"}
    return jsonify({k: storage.count(v) for k, v in tgts.items()})
