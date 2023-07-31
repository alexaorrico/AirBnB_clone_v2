#!/usr/bin/python3
"""
script that create a route /status on the object app_views that returns a JSON
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """create a Json of status"""
    return (jsonify({"status": "OK"}))


@app_views.route('/stats')
def stats():
    """retrieves the number of each objects by type"""
    a = storage.count("Amenity")
    c = storage.count("City")
    p = storage.count("Place")
    r = storage.count("Review")
    s = storage.count("State")
    u = storage.count("User")

    return (jsonify(amenities=a, cities=c, places=p,
                    reviews=r, states=s, users=u))
