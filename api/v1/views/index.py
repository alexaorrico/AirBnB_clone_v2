#!/usr/bin/python3
""" index """

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


@app_views.route('/status', strict_slashes=False)
def status():
    """ returns JSON string """
    return (jsonify({"status": "OK"}))


@app_views.route('/stats', strict_slashes=False)
def stats():
    """ retrieves the number of each objects by type """
    stat_objs = {
            v.__tablename__: storage.count(k) for k, v in classes.items()}
    return (jsonify(stat_objs))
