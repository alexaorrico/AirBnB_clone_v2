#!/usr/bin/python3
"""
Index
"""

from flask import jsonify
from api.v1.views import app_views

from models import storage


@app_views.routes("/status", methods=['GET'], strict_slashes=False)
def status():
    """
    status route
    :return: reposnse with json 
    """
    data = {
        "status": "OK"
    }
    
    resp = jsonify(data)
    resp.status_code = 200
    
    return resp


@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def stats():
    """
    stats of all objs route
    :return: json of all objs
    """
    data = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("Cities"),
        "places": storage.count("Places"),
        "reviews": storage.count("Reviews"),
        "states": storage.count("States"),
        "users": storage.count("Users"),
    }
    
    resp = jsonify(data)
    resp.status_code = 200

    return resp