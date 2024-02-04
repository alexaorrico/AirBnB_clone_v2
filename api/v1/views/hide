#!/usr/bin/python3
""" This module contains route for status of the api
    and statistic of all classes
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.amenity import Amenity
from models.user import User
from models.review import Review
from models.place import Place
from models.city import City


@app_views.route('/status', strict_slashes=False)
def status():
    """ return the status of the API """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """ return the statistic of all class objects in the storage """
    amenities_count = storage.count(Amenity)
    cities_count = storage.count(City)
    places_count = storage.count(Place)
    reviews_count = storage.count(Review)
    states_count = storage.count(State)
    users_count = storage.count(User)

    all_classes_stat = {'amenities': amenities_count,
                        'cities': cities_count,
                        'places': places_count,
                        'reviews': reviews_count,
                        'states': states_count,
                        'users': users_count
                        }
    return jsonify(all_classes_stat)
