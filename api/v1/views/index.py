#!/usr/bin/python3
"""
Creates routes to API objects
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

classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route('/status')
def status():
    """Returns OK status"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def get_stats():
    """
    Endpoint that retrieves the number of ojbects of each
    type.
    """
    class_lib = {}
    for name, clsname in classes.items():
        class_lib[name] = storage.count(clsname)
    return jsonify(class_lib)
