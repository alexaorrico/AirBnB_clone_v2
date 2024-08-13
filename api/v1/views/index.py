#!/usr/bin/python3
"""ind"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


classes = {"amenities": Amenity, "cities": City, "places": Place,
           "reviews": Review, "states": State,
           "users": User}


@app_views.route('/status')
def api_stat():
    """ check """
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def count_stats():
    '''check'''
    stats_count = {}
    for cls in classes:
        stats_count[cls] = storage.count(classes[cls])
    return jsonify(stats_count)