#!/usr/bin/python3
"""
This module imports the app view blueprint and defines
all associated methods with the blueprint
"""
from api.v1.views import app_views
from flask import jsonify
from models import Amenity, City, Place, Review, State, User
from models import storage


@app_views.route("/status")
def api_ok():
    """
    This function simply determines if server
    serving api's is up and running
    """
    return jsonify({"status": "OK"})

# @app_views.route("/stats")
