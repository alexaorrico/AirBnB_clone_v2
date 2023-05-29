#!/usr/bin/python3
""" Provides status of our Flask instance route of 'app' """
from api.v1.views import app_views
from models import storage
from flask import jsonify


@app_views.route("/status")
def app_status():
    """ App status if successful """
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def cool_stats():
    """ Endpoint that retrieves the number of each objects by type """
    return jsonify({
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    })
