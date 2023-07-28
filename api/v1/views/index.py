#!/usr/bin/python3

"""
import app_views from api.v1.views
create a route /status on the object
app_views that returns a JSON: "status": "OK"
"""
from api.v1.views import app_views
from flak import jsonify
from models import storage


@app_views.route("/status")
def status():
    """ returns a JSON format"""
    return jsonify({"status": "OK"})


@app_views.route("/api/v1/stats")
def stats():
    """returns json of all objects"""
    data = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
        }

    res = jsonify(data)
    res.status_code = 200

    return res
