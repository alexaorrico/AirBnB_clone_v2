#!/usr/bin/python3
"""
module that is used for api index page
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def api_status():
    """ returns json string when request api status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def returns_no():
    """returning count for all objects by type"""
    if request.method == 'GET':
        res = {}
        clss = {
            "Amenity": "amenities",
            "City": "cities",
            "Place": "places",
            "Review": "reviews",
            "State": "states",
            "User": "users"
            }
        for k, v in clss.items():
            res[v] = storage.count(k)
        return jsonify(res)
