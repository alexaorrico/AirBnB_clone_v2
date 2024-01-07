#!/usr/bin/python3
"""Blueprint for api status"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    """Returns the api status in JSON format"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    from models.amenity import Amenity
    from models.base_model import BaseModel
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User
    """Returns the number of items in storage in JSON format"""
    from models import storage
    classes = {"amenities": Amenity, "cities": City, "places": Place,
               "reviews": Review, "states": State, "users": User
               }

    all_cls_stats = {key: storage.count(val) for key, val in classes.items()}
    return jsonify(all_cls_stats)
