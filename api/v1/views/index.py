#!/usr/bin/python3
"""
File index.py
"""


from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """Return status"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    """Get the count of all instances by type
    """
    return jsonify({
        "amenities": storage.count('Amenity'),
        "cities": storage.count('City'),
        "places": storage.count('Place'),
        "reviews": storage.count('Review'),
        "states": storage.count('State'),
        "users": storage.count('User')
    })
