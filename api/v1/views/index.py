#!/usr/bin/python3
"""module state"""
from api.v1.views import app_views
from models import storage
import flask


@app_views.route("/status")
def sttus():
    """return status ok"""
    return flask.jsonify({"state": "ok"})


@app_views.route("/stats")
def coun_obj():
    """return obj number"""
    return flask.jsonify({
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
        }
    )
