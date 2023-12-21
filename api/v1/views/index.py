#!/usr/bin/python3
"""Index view for api v1"""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

# route to return JSON status
@app_views.route("/status")
def status():
    """Returns status of API"""
    return jsonify({"status": "OK"})

# route to return JSON stats
@app_views.route("/stats")
def stats():
    """Retrieves number of each objects by type"""

    classes = {"amenities": Amenity, "cities": City, "places": Place,
               "reviews": Review, "states": State, "users": User}
# return dictionary of each object type and number of objects
    return jsonify({key: storage.count(value) for key, value in classes.items()})
