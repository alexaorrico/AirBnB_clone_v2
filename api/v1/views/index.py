#!/usr/bin/python3
"""
returns a JSON: "status": "OK"
"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage as s


@app_views.route('/status', methods=['GET'])
def status_rt():
    """ returns status route ok for GET """
    if request.method == 'GET':
        return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats_rt():
    """ retrieves the number of each objects by type """
    if request.method == 'GET':
        resp = {
                "amenities": s.count(Amenity),
                "cities": s.count(City),
                "places": s.count(Place),
                "reviews": s.count(Review),
                "states": s.count(State),
                "users": s.count(User)
                }
        return jsonify(resp)
