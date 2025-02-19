#!/usr/bin/python3
"""
Imports: app_views, jsonify

app_views(instance): BLueprint instance
jsonify(method): transform objects into JSON
storage(instance): DBStorage() or FileStorage() instance
main app classes: State, Amenity, Places etc
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


@app_views.route('/status', strict_slashes=False)
def status():
    """Return app API status as JSON"""
    status ={
            'status': 'OK'
            }

    return jsonify(status)


@app_views.route('/stat', strict_slashes=False)
def total_objs():
    """Return no of objects of all classes"""
    all_objs = {
            'amenities': storage.count(City)
            'places': storage.count(Place)
            'reviews': storage.count(Review)
            'states': storage.count(State)
            'users': storage.count(User)
            }
    return jsonify(all_objs)
