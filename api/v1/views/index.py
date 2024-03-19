#!/usr/bin/python3
"""
import app_views,
create a route /status on the object
app_views that returns a JSON

"""

from flask import jsonify
from models import storage
from api.v1.views import app_views
from models.city import City
from models.review import Review
from models.user import User
from models.state import State
from models.amenity import Amenity
from models.place import Place


@app_views.route('/status')
def status():
    """return status: OK"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """returns count of models"""
    model_cls = {"amenities": Amenity, "cities": City, "places": Place,
                 "reviews": Review, "states": State, "users": User}
    dict_cls = {key: storage.count(cls) for key,
                cls in model_cls.items()}
    return jsonify(dict_cls)
