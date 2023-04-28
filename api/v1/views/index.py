#!/usr/bin/python3
""" An index file for our Flask API """

from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage

@app_views.route('/status', strict_slashes=False)
def api_status():
    """ A function to return status of the API """
    return jsonify({"status": "OK"})

@app_views.route('/stats', strict_slashes=False)
def obj_stats():
    """ Returns object tally """
    my_dict = {
            "amenities": storage.count(Amenity),
            "cities": storage.count(City),
            "places": storage.count(Place),
            "reviews": storage.count(Review),
            "states": storage.count(States),
            "users": storage.count(User)
            }
    return jsonify(my-dict)
