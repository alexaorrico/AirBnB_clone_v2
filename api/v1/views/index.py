#!/usr/bin/python3
"""Index page of the website"""
from api.v1.views import app_views
from flask import jsonify
from models import storage

storageDict = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"
}


@app_views.route("/status", strict_slashes=False)
def status():
    """handles the status route"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def stats():
    """handle the stats"""
    return jsonify(
        {key: storage.count(value) for key, value in storageDict.items()}
    )


if __name__ == "__main__":
    pass
