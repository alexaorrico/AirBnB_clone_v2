#!/usr/bin/python3
'''root of views'''
from flask import jsonify
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from models.state import State


@app_views.route('/status')
def status():
    '''checks status'''
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def stats():
    '''fetches stats'''
    data = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return jsonify(data)
