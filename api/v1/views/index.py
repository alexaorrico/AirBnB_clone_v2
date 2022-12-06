#!/usr/bin/python3
"""Module that defines routes to be displayed"""
from api.v1.views import app_views
from flask import jsonify
from models import storage

from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'])
def get_status():
    return jsonify({"status": "OK"})


@app_views.route('/api/v1/stats', methods=['GET'])
def stats():
    classes = {
               'amenities': BaseModel, 'users': User, 'places': Place,
               'states': State, 'cities': City, 'amenities': Amenity,
               'reviews': Review
              }
