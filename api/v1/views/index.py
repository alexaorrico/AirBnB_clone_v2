#!/usr/bin/python3
""" first route """

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.user import User
from models.state import State
from models.review import Review


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status_route():
    """ Route that returns a JSON """
    return jsonify({'status': 'OK'})

@app_views.route('/api/v1/stats', methods=['GET'])
def stats():
    count_objs = {
            "amenities": storage.count(Amenity), 
            "cities": storage.count(City), 
            "places": storage.count(Place), 
            "reviews": storage.count(Review), 
            "states": storage.count(State), 
            "users": storage.count(User)
            }
    return jsonify(count_objs)