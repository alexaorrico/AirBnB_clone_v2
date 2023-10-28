#!/usr/bin/python3
"""this is the index file"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

classes = {"users": "User", "places": "Place", "states": "State",
           "cities": "City", "amenities": "Amenity",
           "reviews": "Review"}


@app_views.route('/status', methods=['GET'])
def status():
    '''this is the  route to status page '''
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'])
def count():
    '''this route will retrieve the number of each objs by type'''
    count = {}
    for i in classes:
        count_dict[i] = storage.count(classes[i])
    return jsonify(count)
