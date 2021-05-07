#!/usr/bin/python3
'''Creates route that returns a JSON'''
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

@app_views.route('/status', strict_slashes=False)
def status_check():
    '''returns JSON that has only OK'''
    return jsonify({"status": "OK"})


@app_views.route('/api/v1/stats', strict_slashes=False)
def class_count():
    '''counts number of each kind of class in storage'''
    stats  = {}
    classlist = [State, City, User, Place, Review, Amenity]
    for class_type in classlist:
        stats[type(class_type).__name__] = storage.count(class_type)
    return jsonify(stats)
