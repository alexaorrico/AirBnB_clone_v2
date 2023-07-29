from . import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def count():
    """an endpoint that retrieves the number of each objects by type"""
    return jsonify({
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
        })
