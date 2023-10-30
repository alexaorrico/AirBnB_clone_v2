#!/usr/bin/python3
"""It creates a route /status on the object app_views"""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """It returns a JSON"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def endpoint():
    """It creates an endpoint"""
    return jsonify({"amenities": storage.count("Amenity"),
                    "User": storage.count("User"),
                    "City": storage.count("City"),
                    "Place": storage.count("Place"),
                    "Review": storage.count("Review"),
                    "State": storage.count("State")})
