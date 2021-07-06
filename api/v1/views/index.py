#!/usr/bin/python3
""" Routes of functions """
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def status():
    """ Returns a JSONIFY status ok """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """ Comment """
    obt_types = {"amenities": storage.count('Amenity'),
                 "cities": storage.count('City'),
                 "places": storage.count('Place'),
                 "reviews": storage.count('Review'),
                 "states": storage.count('State'),
                 "users": storage.count('User'),
                 }
    return jsonify(obt_types)
