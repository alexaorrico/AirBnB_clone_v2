#!/usr/bin/python3
"""index for page"""

from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
	"""Function that returns status"""
	return jsonify({"status": "OK"})

@app_views.route('/stats', strict_slashes=False, methods=['GET'])
def stats():
    """Returns JSON 'status and OK"""
    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")})