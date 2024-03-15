#!/usr/bin/python3
"""Module containing API routes"""
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


@app_views.route('/status', strict_slashes=False)
def status():
    res = {"status": "OK"}
    return res


@app_views.route('/stats', strict_slashes=False)
def stats():
    counts = {}
    for cls in classes:
        counts[cls] = storage.count(cls)
    return counts
