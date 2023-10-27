#!/usr/bin/python3
"""Creates routes"""

from api.v1.views import app_views
from flask import jsonify, make_response
from models import storage
from models.amenity import Amenity
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review


@app_views.route('/status')
def status():
    """Returns json rep of response code"""
    return make_response(jsonify({"status": "OK"}), 200)


@app_views.route('/stats')
def count_objects():
    """counts the number of respective object"""
    classes = [Amenity, City, Place, Review, State, User]
    objs = ['amenities', 'cities', 'places', 'reviews', 'states', 'users']
    di_ct = {}
    i = 0
    for key in objs:
        di_ct[key] = storage.count(classes[i])
        i += 1

    return make_response(jsonify(di_ct))
