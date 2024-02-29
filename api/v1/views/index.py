#!/usr/bin/python3
"""
index file
"""
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status", strict_slashes=False)
def status():
    """
    Return a JSON response with status OK
    """
    return jsonify({"status": "OK"})

@app_views.route("/stats", strict_slashes=False)
def stats():
    """
    endpoint that retrieves the number of each objects by type
    """
    classes = {"Amenity": Amenity, "City": City,
               "Place": Place, "Review": Review, "State": State, "User": User}
    objs = {}
    for cls in classes:
        count = storage.count(classes[cls])
        objs[cls] = int(count)
    
    return jsonify(objs)
