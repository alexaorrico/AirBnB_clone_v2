#!/usr/bin/python3
"""index file for app views"""

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
classes = [Amenity, City, Place, Review, State, User]
decoded = ["amenities", "cities", "places", "reviews", "states", "users"]


@app_views.route("/status", strict_slashes=False)
def status_check():
    """
    a route /status on the object app_views that
    returns a JSON: "status": "OK"
    """
    return {"status": "OK"}


@app_views.route("/stats", strict_slashes=False)
def view_counts():
    """an endpoint that retrieves the number of each objects by type"""
    out = {}
    for i in range(len(classes)):
        out.update({decoded[i]: storage.count(classes[i])})
    return out
