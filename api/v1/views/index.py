#!/usr/bin/python3
"""Endpoints of the blueprint app_views"""


from flask import Flask, jsonify
from api.v1.views import app_views



@app_views.route('/status')
def api_status():
    """Endpoint (route) will be to return the status of the API"""
    # We can use json.dump() or flask.jsonify()
    return jsonify({"status":"OK"})

 
@app_views.route('/stats')
def objects_qty():
    """Retrieves the number of each objects by type"""
    from models import storage
    return jsonify({
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    })
