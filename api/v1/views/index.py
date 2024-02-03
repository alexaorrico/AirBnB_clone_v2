#!/usr/bin/python3
'''Holds the index view for the API.'''
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
    '''Retrieves the status of the API.
    '''
    return jsonify(status='OK')


@app_views.route('/stats', methods ['GET'])
def stats():
    '''Retrieves the number of each objects by type'''
    objects = {
        'amenities': Amenity,
        'cities': City,
        'places': Place,
        'reviews': Review,
        'states': State,
        'users': User
    }
    # Using dictionary comprehension to count the objects
    objects = {key: storage.count(value) for key, value in objects.items()}
    return jsonify(objects)
