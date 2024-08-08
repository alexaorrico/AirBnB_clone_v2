#!/usr/bin/python3
"""routes of the app_view blueprint"""
# from api.v1.views import app_views avoid circular import
from flask import jsonify, make_response  # , make_response
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from api.v1.views import app_views


classes = {
  "amenities": Amenity,
  "cities": City,
  "places": Place,
  "reviews": Review,
  "states": State,
  "users": User
}


@app_views.route("/status", strict_slashes=False, methods=["GET"])
def get_status():
    """return status OK"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False, methods=["GET"])
def get_stats():
    """get objects count"""
    stats = {}
    for cls_name, cls in classes.items():
        stats[cls_name] = storage.count(cls)

    return make_response(jsonify(stats))
