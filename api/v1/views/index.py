#!/usr/bin/pyton3
""" Index.py: return json content"""


from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status_ch(self):
    """ Checking status code """
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats_text():
    """Retrives number of each object by type"""
    objects = ({"amenities": storage.count("Amenity"),
                "cities": storage.count("City"),
                "places": storage.count("Place"),
                "reviews": storage.count("Review"),
                "states": strorage.count("State"),
                "users": storage.count("User")})
    return jsonify(objects)
