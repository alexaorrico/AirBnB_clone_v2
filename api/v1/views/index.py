#!/usr/bin/python3
'''module for storing blueprint routes'''
from api.v1.views import app_views
from models import storage
from flask import jsonify
from models.amenity import Amenity
from models.review import Review
from models.place import Place
from models.state import State
from models.city import City
from models.user import User


@app_views.route('/status', strict_slashes=False)
def return_status():
    '''returns status'''
    status = {'status': 'OK'}
    return jsonify(status)


@app_views.route('/stats', strict_slashes=False)
def return_stats():
    '''returns count of objs available of each type'''
    classes = [State, City, User, Place, Review, Amenity]
    stats = {}

    for class_type in classes:
        stats[class_type.__name__] = storage.count(class_type)
    return jsonify(stats)
