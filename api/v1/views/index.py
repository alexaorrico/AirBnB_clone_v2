#!/usr/bin/python3
"""index file"""

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from flask import jsonify

classes = {
           "amenities": Amenity,
           "cities": City,
           "places": Place,
           "reviews": Review,
           "states": State,
           "users": User,
           }


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """API status"""
    return jsonify({"status": "OK"})

@app_views.route('/stats')
def obj_count():
    """retrieve number of objects by type"""
    obj_count = {}
    for key, value in classes.items():
        obj_count[key] = storage.count(value)
    return jsonify(obj_count)


if __name__ == '__main__':
    pass
