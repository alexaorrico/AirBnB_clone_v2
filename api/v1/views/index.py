#!/usr/bin/python3
""" Index for our web flask """
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """ Return json status of web flask """
    return jsonify({'status': 'OK'})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """ Returns json of stats of number of objs """
    return jsonify({'amenities': storage.vount(Amenity)})
