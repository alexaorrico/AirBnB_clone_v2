#!/usr/bin/python3
"""this is a test string"""

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
    """this is a test string"""
    return {"status": "OK"}


@app_views.route("/stats", strict_slashes=False)
def view_counts():
    """this is a test string"""
    out = {}
    for i in range(len(classes)):
        out.update({decoded[i]: storage.count(classes[i])})
    return out
