#!/usr/bin/python3
import json
from models import storage
from flask import Response
from api.v1.views import app_views


@app_views.route("/", strict_slashes=False)
def index():
    """index route of app"""
    return "No entries here so far\n"


@app_views.route("/status", strict_slashes=False)
def status():
    """status method to return status to api request"""
    return Response("{}\n".format(json.dumps({
        "status": "OK"
    })), mimetype='application/json')


@app_views.route("/stats", strict_slashes=False)
def stats():
    """Stats route for flask app"""
    return Response("{}\n".format(json.dumps({
        "amentities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    })))


@app_views.route("<path:invalid_path>")
def not_found(invalid_path):
    """Error handling function for 404 page"""
    return Response("{}\n".format(json.dumps({
        "error": "Not found"
    })))
