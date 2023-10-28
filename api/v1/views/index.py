#!/usr/bin/python3
"""module containing a Flask Blueprint instance routes"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"amenities": Amenity, "cities": City, "places": Place,
           "reviews": Review, "states": State, "users": User}


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns a JSON"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """Returns counts for all resources"""
    return jsonify({obj: storage.count(classes[obj]) for obj in classes})
