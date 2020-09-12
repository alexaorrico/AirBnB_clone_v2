#!/usr/bin/python3
"""Flask"""


from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.amenity import Amenity
from models.user import User


classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route('/status', strict_slashes=False)
def status():
    """status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stat_obj():
    """return statut of obj"""
    num = {}
    for i in range(len(classes)):
        num_objs[names[i]] = storage.count(classes[i])

    return jsonify(num)
