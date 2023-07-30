#!/usr/bin/python3

"""
checks status
"""
from flak import jsonify
from models import storage
from api.v1.views import app_views


@app_views.route("/status")
def status_json():
    """ returns a JSON format"""
    return jsonify({"status": "OK"})


@app_views.route("/api/v1/stats")
def stats_count():
    """returns json of all objects"""
    endpoint_data = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
        }

    res = jsonify(endpoint_data)
    res.status_code = 200
    return res
