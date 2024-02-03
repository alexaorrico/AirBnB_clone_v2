#!/usr/bin/python3
'''
Contains the index view for the API.
'''
from flask import jsonify

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    '''Gets the status of the API.
    '''
    return jsonify({'status': 'OK'})

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    '''Gets the number of objects for each type.
    '''
    object_types = {
        'amenities': Amenity,
        'cities': City,
        'places': Place,
        'reviews': Review,
        'states': State,
        'users': User
    }
    stats = {key: storage.count(value) for key, value in object_types.items()}
    return jsonify(stats)
