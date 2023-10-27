#!/usr/bin/python3
"""Creates routes"""

from api.v1.views import app_views
from flask import jsonify, make_response
from models import storage


@app_views.route('/status')
def status():
    """Returns json rep of response code"""
    return make_response(jsonify({"status": "OK"}), 200)


@app_views.route('/stats')
def count_objects():
    """counts the number of respective object"""
    classes = ['Amenities', 'Cities', 'Places', 'Reviews', 'States', 'Users']
    objs = {'amenities', 'cities', 'places', 'reviews', 'states', 'users'}
    i = 0
    for key in objs:
        objs[key] = storage.count(classes[i])
        i+=1

    return make_response(jsonify({objs}))

