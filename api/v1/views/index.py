#!/usr/bin/python3
"""Routes Controller"""

from api.v1.views import app_views
from models.state import State
from models.amenity import Amenity
from models.review import Review
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
from models import storage
from flask import jsonify


Classes = {'states': State, 'users': User, 'amenities': Amenity,
           'reviews': Review, 'cities': City, 'places': Place}


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """API status"""
    return jsonify(status='OK')


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """API stats"""
    class_dict = {}
    for key, cls in Classes.items():
        class_dict[key] = storage.count(cls)
    return jsonify(class_dict)
