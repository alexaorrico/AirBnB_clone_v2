#!/usr/bin/python3
"""A route that will display the status code"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    objs = {
        "amenities": storage.count(State),
        "cities": storage.count(City),
        "place": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": torage.count(User)
    }
    return jsonify(objs)
