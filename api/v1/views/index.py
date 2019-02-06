#!/usr/bin/python3
"""return index"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status_ret():
    """return json"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stat_ret():
    """return number of stat"""
    count_am = storage.count("Amenity")
    count_ct = storage.count("City")
    count_pl = storage.count("Place")
    count_re = storage.count("Review")
    count_st = storage.count("State")
    count_us = storage.count("User")
    return jsonify({"amenities": count_am,
                    "cities": count_ct,
                    "places": count_pl,
                    "reviews": count_re,
                    "states": count_st,
                    "users": count_us})
