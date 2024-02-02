#!/usr/bin/python3
"""
a route /status on the object app_views
returns a JSON: "status": "OK" (see example)
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status',  methods=['GET'])
def index():
    return jsonify({"status": "OK"})


@app_views.route('/stats',  methods=['GET'])
def index():
    """an endpoint that retrieves the number of each objects by type:"""
    response = {}
    key_val = {
            "Amenity": "amenities",
            "City": "cities",
            "Place": "places",
            "Review": "reviews",
            "State": "states",
            "User": "users"
        }

    for key, val in key_val.items():
        response[val] = storage.count(key)
    return jsonify(response)
