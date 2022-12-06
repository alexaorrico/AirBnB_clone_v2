#!/usr/bin/python3
'''
Module contains the routes to be used for the API.
'''

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity

classes = {"amenities": Amenity, "cities": City, "places": Place,
           "reviews": Review, "states": State, "users": User}


@app_views.route('/status')
def app_status():
    '''Returns the status code.'''
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def count():
    '''Returns the count of objects from storage.'''
    class_count_dict = {}
    for key, cls_name in classes:
        cls_count = storage.count(cls_name)
        class_count_dict[key] = cls_count
    return jsonify(class_count_dict)
