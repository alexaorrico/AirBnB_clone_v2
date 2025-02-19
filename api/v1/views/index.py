#!/usr/bin/python3
<<<<<<< HEAD
"""index """
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Status of API """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def number_objects():
    """ Retrieves the number of each objects by type """
    classes = [Amenity, City, Place, Review, State, User]
    names = ["amenities", "cities", "places", "reviews", "states", "users"]

    num_objs = {}
    for i in range(len(classes)):
        num_objs[names[i]] = storage.count(classes[i])

    return jsonify(num_objs)
=======
""" 
The Index file
"""

from api.v1.views import app_views
from models import storage
from flask import jsonify

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ 
    Returns JSON format
    """
    return jsonify(status="OK")

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """ 
    This method returns the number of each instance type 
    """
    return jsonify(amenities=storage.count("Amenity"),
                   cities=storage.count("City"),
                   places=storage.count("Place"),
                   reviews=storage.count("Review"),
                   states=storage.count("State"),
                   users=storage.count("User"))
>>>>>>> c18aee22ec56a82b2b1c541e9134627845d1d329
