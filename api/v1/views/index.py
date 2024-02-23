#!/usr/bin/python3
""" api/v1/views/index.py """
from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    return jsonify({"status": "OK"})

