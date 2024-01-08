#!/usr/bin/python3
"""Index view"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """Returns the status of the API"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def get_objets():
    """Retrieves the number of each objects by type"""
    from models import storage
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User
    classes = {"amenities": Amenity, "cities": City, "places": Place,
               "reviews": Review, "states": State, "users": User}
    num_of_objects = classes.copy()
    for key, value in classes.items():
        num_of_objects[key] = storage.count(value)
    return jsonify(num_of_objects)
