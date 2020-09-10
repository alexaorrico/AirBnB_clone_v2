#!/usr/bin/python3
"""
[index page]
"""

from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from models.state import State
from models import storage
from flask import jsonify
from api.v1.views import app_views


classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}

@app_views.route('/status')
def status():
    """[status]

    Returns:
        [type]: [string]
    """
    return jsonify({"status": "OK"})

@app_views.route('/stats')
def nobj():
    """[retrieve the number of each objects by type]
    """
    nobjs = {}
    for obj in classes:
        nobjs[obj] = storage.count(classes[obj])
    return jsonify(nobjs)
