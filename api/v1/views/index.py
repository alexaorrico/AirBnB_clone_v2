#!/usr/bin/python3
"""
routes module
"""
from flask import jsonify
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


@app_views.route("/status", methods=['GET'])
def status():
    ''' returns status code of the api '''
    return jsonify(status="OK")


@app_views.route("/stats", methods=['GET'])
def stats():
    '''return stats of objects'''
    dict = {}
    for key, cls in classes.items():
        dict[key] = storage.count(cls)
    return jsonify(dict)
