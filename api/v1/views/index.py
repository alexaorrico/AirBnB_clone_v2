#!/usr/bin/python3
'''creates route on the object app_views and returns json'''
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity
from models import storage
from flask import jsonify


@app_views.route('/status')
def status():
    '''status - shows status ok'''
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    '''stats - shows num of each object by type'''
    return jsonify({"amenities": storage.count(Amenity),
                    "cities": storage.count(City),
                    "places": storage.count(Place),
                    "reviews": storage.count(Review),
                    "states": storage.count(State),
                    "users": storage.count(User)
                    })
