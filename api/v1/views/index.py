#!/usr/bin/python3
'''
route /status on the object app_views
that returns a JSON: "status": "OK"
'''

from api.v1.views import app_views
from flask import jsonify, request
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    '''returns status'''
    if request.method == 'GET':
        resp = {'status': 'OK'}
        return jsonify(resp)

@app_views.route('/stats', methods=['GET'])
def stats():
    '''returns count of all class objects'''
    if request.method == 'GET':
        response = {}
        PLURALS = {
                'Amenity': 'amenities',
                'City': 'cities',
                'Place': 'places',
                'Review': 'reviews',
                'State': 'states',
                'User': 'users'
                }
        for k, v in PLURALS.items():
            response[v] = storage.count(k)
        return jsonify(response)
