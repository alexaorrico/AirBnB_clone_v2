#!/usr/bin/python3
"""Index"""
from models import storage
from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', strict_slashes=False)
def status():
    """ Status of API """
    ok_status = {"status": "OK"}
    return jsonify(ok_status)


@app_views.route('/stats')
def stats():
    """
        return dict count of data
    """
    my_dict = {"amenities": storage.count(Amenity),
               "cities": storage.count(City),
               "places": storage.count(Place),
               "reviews": storage.count(Review),
               "states": storage.count(State),
               "users": storage.count(User)}
    return jsonify(my_dict)
