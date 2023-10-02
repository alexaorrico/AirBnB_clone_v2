#!/usr/bin/python3
"""
This Module handles the status route endpoint
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.user import User
from models.review import Review

classes = {
        "states": State,
        "cities": City,
        "amenities": Amenity,
        "places": Place,
        "users": User,
        "reviews": Review
        }


@app_views.route('/status')
def status():
    """returns the status of a request"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def object_no():
    """ retrieves the number of each objects based on its type """
    objs_count = {}
    for key, cls in classes.items():
        n = storage.count(cls)
        objs_count[key] = n
    return jsonify(objs_count)
