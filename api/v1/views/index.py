#!/usr/bin/python3
"""Docstring for index"""
from flask import Flask, jsonify
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False, methods=['GET'])
def get_status():
    """returns a JSON: 'status': 'OK'"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats', strict_slashes=False, methods=['GET'])
def get_stats():
    """returns a JSON: 'class': count"""
    from models import storage
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User

    my_dict = {}
    class_names = {'amenities': Amenity, 'cities': City, 'places': Place,
                   'reviews': Review, 'states': State, 'users': User}

    for k, v in class_names.items():
        my_dict.update({k: storage.count(v)})

    return jsonify(my_dict)
