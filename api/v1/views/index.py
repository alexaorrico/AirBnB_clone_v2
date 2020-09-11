#!/usr/bin/python3
"""
Here is where we create the routes 
to the endpoints of our blueprints
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


classes = {"amenities": Amenity, "cities": City, "places": Place,
           "reviews": Review, "states": State, "users": User}


# the followings are the entendpoints of the app_view blueprint
# in other words /status == /api/v1/status and /stats == /api/v1/stats
# we create that blueprint to access to all the endpoints easily

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """ returns status """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """
    function to return the count of all class objects
    """
    result = {}
    for key, value in classes.items():
        result[key] = storage.count(value)
    return jsonify(result)


if __name__ == "__main__":
    pass
