#!/usr/bin/python3
"""Create routes and save JSON package"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def app_view_json():
    """ object app_views that returns a JSON """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def cout_data_json():
    """ comment function app views """
    return jsonify({"amenities": storage.count("Amenity"),
                    "states": storage.count("State"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "users": storage.count("User")})
