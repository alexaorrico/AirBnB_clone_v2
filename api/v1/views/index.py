#!/usr/bin/python3
"""
This module shows roots for our site
"""
from flask import Flask, jsonify
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
app = Flask(__name__)


@app_views.route('/status')
def status():
    """Returns status of the website if running"""
    status = {'status': 'OK'}
    return jsonify(status)


@app_views.route('/stats')
def stats():
    stats = {'amenities': storage.count(Amenity),
             'cities': storage.count(City),
             'places': storage.count(Place),
             'reviews': storage.count(Review),
             'states': storage.count(State),
             'users': storage.count(User)}
    return jsonify(stats)
