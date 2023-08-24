#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route('/status', methods=['GET'])
def get_status():
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'])
def get_stats():
    dic = { "amenities": "Amenity", "cities": "City",
            "places": "Place", "reviews": "Review",
            "states": "State", "users": "User"}
    
    ret = {}
    for k, v in dic.items():
        ret[k] = storage.count(v)
    return jsonify(ret)
