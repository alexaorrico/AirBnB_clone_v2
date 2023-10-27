#!/usr/bin/python3
"""our index file"""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def status():
    """
    import app_views from api.v1.views
create a route /status on the object app_views that returns a JSON: "status": "OK" (see example)
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """an endpoint that retrieves the number of each objects by type"""

    class_list = {
        "User": "users",
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
    }
    cl_list = ["User", "Amenity", "City", "Place", "Review", "State"]
    count_dict = {}

    for class_name in class_list.keys():
        count_dict[class_list[class_name]] = storage.count(class_name)

    return jsonify(count_dict)
