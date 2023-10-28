#!/usr/bin/python3
""" API status"""
from api.v1.views import app_views
from flask import jsonify
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """ Return OK"""
    return jsonify(status='OK')


@app_views.route('/stats', strict_slashes=False)
def count_obj():
    '''Json '''
    objs = {
        'states': State, 'users': User,
        'amenities': Amenity, 'cities': City,
        'places': Place, 'reviews': Review
    }
    for key in objs:
        objs[key] = storage.count(objs[key])
    return jsonify(objs)
