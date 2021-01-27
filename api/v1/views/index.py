#!/usr/bin/python3
"""returns the status of the API
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage

from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

@app_views.route('/status/', strict_slashes=False)
def status():
    """returns status: OK if JSON is working
    """
    json_status = {"status": "OK"}
    return jsonify(json_status)


@app_views.route('/stats/', strict_slashes=False)
def stats():
    """endpoint that retrieves the number of each objects by type
    """
    json_stats = {
        "amenities": storage.count('Amenity'),
        "cities": storage.count('City'),
        "places": storage.count('Place'),
        "reviews": storage.count('Review'),
        "states": storage.count('State'),
        "users": storage.count('User')
    }

    return jsonify(json_stats)
