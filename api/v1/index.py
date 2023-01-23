#!/usr/bin/python3
'''Contains the index view for the API.'''
from flask import jsonify

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def get_status():
    '''returns the status of the API.
    '''
    return jsonify(status='OK')


@app_views.route('/stats')
def get_stats():
    ''' an endpoint that retrieves the '''
    '''number of each objects by type:'''
    model_obj = {
        'amenities': Amenity,
        'cities': City,
        'places': Place,
        'reviews': Review,
        'states': State,
        'users': User
    }
    for key, val in model_obj.items():
        model_obj[key] = storage.count(val)
    return jsonify(model_obj)
