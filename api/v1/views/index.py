#!/usr/bin/python3
"""
an endpoint that retrieves the number of each objects by type
"""
from flask import jsonify
from models import classes
from models import storage
from api.v1.views import app_views


@app_views.route("/status")
def status():
    """
    return status in json
    """
    stat = {"status": "OK"}
    return (jsonify(stat))


@app_views.route("/stats")
def stats():
    """
    endpoint that retrieves number of obj by type
    """
    dic = {"amenities": 0, "cities": 0, "places": 0,
           "reviews": 0, "states": 0, "users": 0}
    cls = ["Amenity", "City", "Place", "Review", "State", "User"]
    st = ["amenities", "cities", "places", "reviews", "states", "users"]
    for c in range(len(cls)):
        try:
            dic[st[c]] = storage.count(cls[c])
        except Exception:
            continue
    return (jsonify(dic))
