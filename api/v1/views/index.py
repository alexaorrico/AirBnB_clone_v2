#!/usr/bin/python3

"""
create a route /status on the object app_views
returns a JSON "status": "OK"
"""


from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def status():
    """
    returns JSON: "status": "OK"
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """
    retrieves the number of each objects by type
    """
    obj_count = {
            "amenities": storage.count(Amenity),
            "cities": storage.count(City),
            "places": storage.count(Place),
            "reviews": storage.count(Review),
            "states": storage.count(State),
            "users": storage.count(User)
            }
    return jsonify(obj_count)
