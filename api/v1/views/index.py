#!/usr/bin/python3
'''API status'''

from flask import jsonify
from api.v1.views import app_views
from models.state import State
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models import storage

@app_views.route('/status', strict_slashes=False)
def return_status():
    '''Return API status'''
    return jsonify(status='OK')

@app_views.route('/stats', strict_slashes=False)
def get_stats():
    '''Return statistics about various models'''
    models = {
        'states': State,
        'users': User,
        'amenities': Amenity,
        'cities': City,
        'places': Place,
        'reviews': Review
    }
    stats = {key: storage.count(cls) for key, cls in models.items()}
    return jsonify(stats)
