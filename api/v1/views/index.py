#!/usr/bin/python3
"""

"""
from api.v1.views import app_views
from flask import jsonify


classes = {
    Amenity: "amenities",
    City: "cities",
    Place: "places",
    Review: "reviews",
    State: "states",
    User: "users"
}


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status_code():
    """
    status route
    """
    status = {"status": "OK"}
    response = jsonify(status)
    return response


@app_views.route("/stats", strict_slashes=False)
def count_objects():
    count_dict = {}
    for obj, value in classes.items():
        count_dict[value] = storage.count(obj)
    return jsonify(count_dict)
