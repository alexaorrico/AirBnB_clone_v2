#!/usr/bin/python3
"""
for rendering js content
"""
from flask import jsonify
from api.v1.views import app_views
from flask import Flask
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """return a json representation of an object"""
    return jsonify("status":"Ok")

@app_views.route('/stats', strict_slashes=False)
def count():
	"""Endpoint to  retrieve the number of each object by type"""
	return jsonify({"amenities": storage.count("Amenity"),
			"cities": storage.count("City"),
			"places": storage.count("Place"),
			"reviews": storage.count("Review"),
			"states": storage.count("State"),
			"users": storage.count("User")})
