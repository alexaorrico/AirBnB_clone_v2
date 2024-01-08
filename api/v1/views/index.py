#!/usr/bin/python3
"""This file returns the JSON status ok"""

from flask import jsonify

<<<<<<< Updated upstream
<<<<<<< Updated upstream
from api.v1.views import app_views

=======
=======
>>>>>>> Stashed changes
import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes

@app_views.route('/status', strict_slashes=False)
def index():
    """home screen of the app"""
    return jsonify({"status": "OK"})

@app_views.route('/stats', strict_slashes=False)
def num_objects():
    result = {}
    for key, value in classes.items():
        total = storage.count(value)
        result[key] = total
    return jsonify(result)
