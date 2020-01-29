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
    status = {"amenities": storage.count("amenities"),
              "cities": storage.count("cities"),
              "places": storage.count("places"),
              "reviews": storage.count("reviews"),
              "states": storage.count("states"),
              "users": storage.count("users")
              }
    return jsonify(status)
