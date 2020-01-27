#!usr/bin/python3
from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route('/status', methods=['GET'])
def get_status():
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'])
def get_stats():
    objects = {
        "amenities": 0,
        "cities": 0,
        "places": 0,
        "reviews": 0,
        "states": 0,
        "users": 0
    }
    for key in objects.keys():
        objects[key] = storage.count(key[0].upper+key[1:])
    return jsonify(objects)

