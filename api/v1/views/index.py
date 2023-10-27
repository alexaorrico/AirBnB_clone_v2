#!/usr/bin/python3
"""This defines routes for blueprint"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """This returns the status of the application"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """This retrieves count of objects in the storage"""
    from models.place import Place
    from models.review import Review
    from models.amenity import Amenity
    from models.city import City
    from models.state import State
    from models.user import User

    classes = {"places": Place, "reviews": Review,
               "amenities": Amenity, "cities": City,
               "states": State, "users": User}
    json_dictionary = {}

    for name, cls in classes.items():
        json_dictionary.update({name: storage.count(cls)})

    return jsonify(json_dictionary)
