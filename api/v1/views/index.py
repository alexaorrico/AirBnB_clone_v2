#!/usr/bin/python3
""" Status of your API """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def app_status():
    '''
    Returns the Status of the API
    '''
    return(jsonify(status="OK"))


@app_views.route("/stats")
def stats():
    '''
    Returns stats
    '''
    total = {"amenities": storage.count("Amenity"),
             "cities": storage.count("City"),
             "places": storage.count("Place"),
             "reviews": storage.count("Review"),
             "states": storage.count("State"),
             "users": storage.count("User")}
    return jsonify(total)
