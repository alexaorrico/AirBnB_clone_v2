#!/usr/bin/python3
""" script index.py"""

from flask import jsonify, make_response
from models import storage
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.state import State
from api.v1.views import app_views

classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route('/status')
def status():
    """ route that return status """
    return make_response(jsonify({'status': 'OK'}), 200)


@app_views.route('/stats')
def stats():
    """ length of resources """
    r_dict = {}

    for cls_name, cls in classes.items():
        r_dict[cls_name] = storage.count(cls)

    return make_response(jsonify(r_dict), 200)
