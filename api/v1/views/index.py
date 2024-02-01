#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify

status = {
    "status": "OK",
}
@app_views.route('/status')
def status():
    """Returns status"""
    return jsonify(status)

@app_views.route('/stats')
def stats():
    """Returns stats"""
    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")})
