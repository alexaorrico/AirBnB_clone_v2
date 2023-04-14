#!/usr/bin/python3
'''
Check the status
'''

from api.v1.views import app_views 
from flask import jsonify
from models import storage

@app_views.route('/status')
def status_ckeck():
    '''check the view status'''
    status = {
            'status':'OK'
            }
    return jsonify(status)

@app_views.route('/api/v1/stats')
def obj_count(): 
    '''Retrieves the number of each objects by type'''
    obj = {
            'amenities': storage.count('Amenity'),
            'cities': storage.count('City'),
            'places': storage.count('Place'),
            'reviews': storage.count('Review'), 
            'states': storage.count('State')
            'users': storage.count('User')
            }
    return jsonify(obj)

