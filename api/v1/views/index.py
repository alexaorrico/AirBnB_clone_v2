#!/usr/bin/python3
"""Defines the API routes for the Flask app"""

from flask import jsonify, Blueprint
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.state import State
from models.review import Review
from models.place import Place
from models.user import User


# Create a blueprint for the API views
app_views = Blueprint('app_views', __name__)


@app_views.route('/status', methods=['GET'])
def get_status():
    """Return the status of the API"""
    # Return a JSON object with the status of the API
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'])
def get_stats():
    """Return the number of objects in the data store for each model"""
    # Create a dictionary with the count of objects for each model
    stats = {
        'amenities': storage.count(Amenity),
        'cities': storage.count(City),
        'places': storage.count(Place),
        'reviews': storage.count(Review),
        'states': storage.count(State),
        'users': storage.count(User),
    }
    # Return a JSON object with the count of objects for each model
    return jsonify(stats)
