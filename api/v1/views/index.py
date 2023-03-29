#!/usr/bin/python3
""" index file """
from api.v1.views import app_views
import json
from models import storage
from flask import jsonify


@app_views.route('/status')
def status():
    dic = {'status': 'OK'}
    return json.dumps(dic, indent=2)


@app_views.route('/stats')
def count():
    dic = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
    }
    return json.dumps(dic, indent=2)
