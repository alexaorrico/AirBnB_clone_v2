#!/usr/bin/python3xx
'''this script for api status'''
import models
from models import storage
from models.base_model import BaseModel
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def api_status():
    '''
    Returns a JSON response for RESTful API health.
    '''
    response = {'status': 'OK'}
    return jsonify(response)
 

@app_views.route('/stats', methods=['GET'])
def get_stats():
    '''
    Retrieves the number of each objects by type.
    '''
    stats = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
    }
    return jsonify(stats)
