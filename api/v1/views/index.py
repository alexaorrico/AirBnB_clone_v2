#!/usr/bin/python3
"""ALX SE Flask Api Module."""
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
        'states': State,
        'users': User
        }


@app_views.route('/status', strict_slashes=False)
def server_status():
    """Return the server status."""
    return jsonify({'status': 'OK'})


@app_views.route('/stats', strict_slashes=False)
def models_stats():
    """Return statistic of all models."""
    stats = {}
    for name, model in models.items():
        total_obj = storage.count(model)
        stats[name] = total_obj
    return jsonify(stats)
