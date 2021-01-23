#!/usr/bin/python3

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
classes = [Amenity, City, Place, Review, State, User]


@app_views.route("/status", strict_slashes=False)
def a():
    """x"""
    return {"status": "OK"}


@app_views.route("/stats", strict_slashes=False)
def b():
    """x"""
    out = {}
    for cls in classes:
        out.update({cls.__name__: storage.count(cls)})
    return out
