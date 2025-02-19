#!/usr/bin/python3
"""index file"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

classes = {
    "users": User,
    "places": Place,
    "states": State,
    "cities": City,
    "amenities": Amenity,
    "reviews": Review
}


@app_views.route('/status')
def status():
    ''' status route '''
    status = {'status': 'OK'}
    return jsonify(status)


@app_views.route('/stats')
def count_stats():
    """Count stats"""
    counter_of_stats = {}
    for class_name, class_ in classes.items():
        counter_of_stats[class_name] = storage.count(class_)
    return jsonify(counter_of_stats)
