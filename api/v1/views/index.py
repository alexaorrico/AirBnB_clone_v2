#!/usr/bin/python3
""" Create a Index """
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


@app_views.route("/status")
def status():
    """Returns status in jason format"""
    return jsonify({'status': 'OK'})


@app_views.route("/stats")
def stats():
    """return count objects"""
    names = {'users': storage.count(User),
             'places': storage.count(Place),
             'states': storage.count(State),
             'cities': storage.count(City),
             'amenities': storage.count(Amenity),
             'reviews': storage.count(Review)}

    return jsonify(names)
