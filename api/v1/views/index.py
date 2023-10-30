#!/usr/bin/python3
"""Flask route for index model"""

from api.v1.views import app_views
from flask import request, jsonify
from models import storage

@app_views.route("/status", method=["GET"])
def status():
    """request status route"""
    if request.method == "GET":
        return jsonify({"status": "OK"})


app_views.route("/stats", method=["GET"])
def stats():
    """an endpoint that retrieves the number of each objects by type:"""
    if request.method == "GET":
        result = {}
        request["amenities"] = storage.count("Amenity")
        request["cities"] = storage.count("City")
        request["places"] = storage.count("Place")
        request["reviews"] = storage.count("Review")
        request["states"] = storage.count("State")
        request["users"] = storage.count("User")
        return jsonify(result)
