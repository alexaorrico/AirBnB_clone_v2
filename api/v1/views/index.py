#!/usr/bin/python3
"""File"""

from flask import Flask, jsonify
from api.v1.views import app_views
import models
from models import storage


@app_views.route('/status')
def status():
    """Route /status on the object app_views that returns a
     JSON: "status": "OK"""""
    status = {"status": "OK"}
    return jsonify(status)


@app_views.route('/stats')
def stats():
    """An endpoint that retrieves the number of each objects by type"""""
    status = {"amenities": storage.count("Amenity"),
              "cities": storage.count("City"),
              "places": storage.count("Place"),
              "reviews": storage.count("Review"),
              "states": storage.count("State"),
              "users": storage.count("User")
              }
    return jsonify(status)
