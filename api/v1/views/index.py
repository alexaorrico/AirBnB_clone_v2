#!/usr/bin/python3
"""index file for the api views"""

from api.v1.views import app_views
from flask import jsonify, request
from models import storage



@app_views.route('/status', methods=['GET'])
def status():
    """
    endpoint for the /status route
    """

    if request.method == 'GET':
        return jsonify({"status": "Ok"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """
    endpoint that retrieves the number of each object by type
    """

    data = {}

    objects = {
      "Amenity": "amenities",
      "City": "cities",
      "Place": "places",
      "Review": "reviews",
      "State": "states",
      "User": "users"
    }

    for key, value in objects.items():
       data[value] = storage.count(key)
    return jsonify(data)
