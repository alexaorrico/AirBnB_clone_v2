#!/usr/bin/python3
'''Creates various routes and returns respective JSONs'''
from api.v1.views import app_views
from flask import jsonify
from models import storage


classes = {"amenities": "Amenity", "cities": "City",
           "places": "Place", "reviews": "Review",
           "states": "State", "users": "User"}


@app_views.route('/status', strict_slashes=False)
def status():
    '''Returns a JSON with status: OK'''
    return jsonify(dict(status="OK"))


@app_views.route('/stats')
def stats():
    ''' Returns a JSON object of counts of classes '''
    counts = {}
    for clss, cls in classes.items():
        obj_count = storage.count(cls)
        counts[clss] = obj_count
    return jsonify(counts)
