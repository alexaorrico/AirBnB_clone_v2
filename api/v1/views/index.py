#!/usr/bin/python3
'''
index page for flask
displays status and stats
'''
from flask import Flask, jsonify, make_response
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def getStatus():
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def getCount():
    count_dict = {"amenities": 'Amenity',
                  "cities": 'City',
                  "places": 'Place',
                  "reviews": 'Review',
                  "states": 'State',
                  "users": 'User'}

    for k in count_dict.keys():
        count_dict[k] = storage.count(count_dict.get(k))
    return jsonify(count_dict)
