#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route('/status', strict_slashes=False)
def status():
    """returns a JSON"""
    dicti = {'status': 'OK'}
    return jsonify(dicti)

@app_views.route('/stats', strict_slashes=False)
def count_ap():
    """retrieves the number of each objects by type"""
    dic = {'amenities': storage.count('Amenity'),
           'cities': storage.count('City'),
           'places': storage.count('Place'),
           'reviews': storage.count('Review'),
           'states': storage.count('State'),
           'users': storage.count('User')}
    return jsonify(dic) 
