#!/usr/bin/python3
'''
    return json
'''


from api.v1.views import app_views
from flask import jsonify
from models import storage


cls = {
    "amenities": 47,
    "cities": 36,
    "places": 154,
    "reviews": 718,
    "states": 27,
    "users": 31
}


@app_views.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def retrieve_json():
    new_dict = {}
    for k, v in cls.items():
        new_dict[k] = storage.count(v)
        return jsonify(new_dict)
