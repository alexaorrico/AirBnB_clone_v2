#!/usr/bin/python3
""" views functionality
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from flask import jsonify, make_response
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'])
def status():
    """ return status OK on route /status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """ returns count of all objects per class"""
    classes = {"amenities": Amenity, "cities": City, "places": Place,
               "reviews": Review, "states": State, "users": User}

    obj_count = {key: storage.count(value) for key, value in classes.items()}
    return make_response(jsonify(obj_count))
