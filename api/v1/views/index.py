#!/usr/bin/python3

"""  views index module """

from api.v1.views import app_views
from models import storage
from flask import jsonify
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"amenities": Amenity,
           "cities": City,
           "places": Place,
           "reviews": Review,
           "states": State,
           "users": User}


@app_views.route('/status', strict_slashes=False, methods=['GET'])
def api_status():
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False, methods=['GET'])
def api_stats():
    dict_stats = {}
    for key, value in classes.items():
        count = storage.count(value)
        dict_stats.update({key: count})
    return jsonify(dict_stats)
