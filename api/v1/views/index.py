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


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """An endpoint that retrieves the number of each objects by type:"""
    classes = {
        "amenity": Amenity,
        "city": City,
        "place": Place,
        "review": Review,
        "state": State,
        "user": User
    }

    obj_cout = {}
    for key, value in classes.items():
        obj_cout[key] = models.storage.count(value)

    return jsonify(obj_cout)
