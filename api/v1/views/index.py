#!/usr/bin/python3
'''
    return json
'''


from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def retrieve_json():
    new_dict = {
        "amenities": storage.count('Amenity'),
        "cities": storage.count('cities'),
        "places": storage.count('palces'),
        "reviews": storage.count('reviews'),
        "states": storage.count('states'),
        "users": storage.count('users'),
    }
    for k, v in new_dict.items():
        new_dict[k] = storage.count(v)
    return jsonify(new_dict)
