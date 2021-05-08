#!/usr/bin/python3
"""Index file that returns a JSON status"""

from api.v1.views import app_views
from flask import Flask
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def status():
    """Method that returns a JSON status"""
    return jsonify(status='OK')


@app_views.route('/stats')
def count():
    """ Returns number of each class """
    stats = {
             "amenities": storage.count(Amenity),
             "cities": storage.count(City),
             "places": storage.count(Place),
             "reviews": storage.count(Review),
             "states": storage.count(State),
             "users": storage.count(User),
            }
    return jsonify(stats)
