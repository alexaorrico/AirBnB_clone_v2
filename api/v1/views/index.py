#/usr/bin/python3
""" Routes of app.py """

from api.v1.views import app_views
from flask import make_response, Flask, jsonify, Blueprint
from json import dumps
from models import storage


classes = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"
}


@app_views.route("/status", strict_slashes=False)
def json_ok():
    """ Return the status of the api """
    response = make_response({"status": "ok"})
    response.headers['Content-Type'] = 'application/json'
    return response


@app_views.route("/stats", strict_slashes=False)
def stats():
    """ returns the count of existing classes """
    dict_count = {}
    for k, v in classes.items():
        dict_count[k] = storage.count(v)
    return jsonify(dict_count)
