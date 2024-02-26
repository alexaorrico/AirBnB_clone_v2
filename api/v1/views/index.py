#!/usr/bin/python3
"""
    Index view of views module
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
        Returns status
    """
    return jsonify(status="OK")


@app_views.route('/stats', strict_slashes=False)
def stats():
    """
        Simple stats for the web app
    """
    objects = {'users': User,
               'cities': City,
               'places': Place,
               'reviews': Review,
               'states': State,
               'users': User
               }
    for obj in objects:
        objects[obj] = storage.count(objects[obj])
    return jsonify(objects)
