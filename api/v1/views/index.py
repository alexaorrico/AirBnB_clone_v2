#!/usr/bin/python3
'''api status'''
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.state import State
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def api_status():
    '''return API status'''
    return jsonify(status='OK')


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def api_stats():
    '''return JSON responses'''
    classes = {
        'states': State,
        'users': User,
        'amenities': Amenity,
        'cities': City,
        'places': Place,
        'reviews': Review
    }
    stats = {key: storage.count(cls) for key, cls in classes.items()}
    return jsonify(stats)

