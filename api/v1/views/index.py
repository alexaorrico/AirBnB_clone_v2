#!/usr/bin/python3
""" index.py """


from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """Returns a JSON string"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """Returns a JSON string"""
    from models import storage
    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")})
