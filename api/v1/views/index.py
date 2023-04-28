#!/usr/bin/python3
"""Index file for package views"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


models = {
        'amenities': Amenity,
        'cities': City,
        'places': Place,
        'reviews': Review,
        'users': User,
        'states': State
        }


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """Return the server status"""
    return jsonify(status="OK")


@app_views.route('/stats', strict_slashes=False)
def get_stats():
    """Return stats of all models"""
    stats = {}
    for name, model in models.items():
        total = storage.count(model)
        stats[name] = total
    return jsonify(stats)
