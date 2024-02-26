#!/usr/bin/python3
"""index for blueprint"""
from api.v1.views import app_views
from flask import jsonify
import models
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Status of API """
    return jsonify({"status": "OK"})

@app_views.route('/stats')
def stats():
    """An endpoint that retrieves the number of each objects by type:"""
    classes = {
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
        "User": "users"
    }
    
    obj_cout = {}
    for key, value in classes.items():
        obj_cout[value] = models.storage.count(key)
    
    return jsonify(obj_cout)
