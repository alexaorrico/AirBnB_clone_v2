#!/usr/bin/python3
"""
Status of our Api and some stats.
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def app_status():
    """
    Simply returns the state of the api.
    """
    return(jsonify(status="OK"))

<<<<<<< HEAD
@app_views.route("/stats")
=======

@app_views.route("/api/v1/stats")
>>>>>>> 243c48b470bf5461b394c3a4afafba2dff00be12
def stats():
    total = {"amenities": storage.count("Amenity"),
             "cities": storage.count("City"),
             "places": storage.count("Place"),
             "reviews": storage.count("Review"),
             "states": storage.count("State"),
             "users": storage.count("User")}
    return jsonify(total)
