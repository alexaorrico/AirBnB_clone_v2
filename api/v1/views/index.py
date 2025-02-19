#!/usr/bin/python3
""" Initialize the views """
from api.v1.views import app_views
from flask import jsonify, make_response
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ retuen the status of the api"""
    data = {"status": "ok"}
    res = jsonify(data)
    res.status_code = 200
    return make_response(res)


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """ check the stats of
    objects by type """
    data = {
            "amenities": storage.count('Amenity'),
            "cities": storage.count('City'),
            "places": storage.count('Place'),
            "reviews": storage.count('Review'),
            "states": storage.count('State'),
            "users": storage.count('User')
            }
    jsdata = jsonify(data)
    return make_response(jsdata)
