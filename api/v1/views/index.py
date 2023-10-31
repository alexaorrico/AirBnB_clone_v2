#!/usr/bin/python3
"""index.py to connect to API"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage


@app_views.route('/status', strict_slashes=False)
def status_ok():
    """Status Ok method

    :return: it returns json status ok message
    """
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'])
def get_objS_stats():
    """
    Get statistics about the total number of objects of each type

    :return: A JSON response containing the number of each object type.
    :rtype: flask.Response
    """
    if request.method == 'GET':
        cls_objs = {
                "Amenity": "amenities",
                "City": "cities",
                "Place": "places",
                "Review": "reviews",
                "State": "states",
                "User": "users"
                }

        response = {value: storage.count(key)
                for key, value in cls_objs.items()}
        return jsonify(response)
