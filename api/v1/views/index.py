#!/usr/bin/python3
"""Index-Status"""

from . import Amenity
from . import app_views
from . import City
from . import Place
from . import Review
from . import State
from . import storage
from . import User


@app_views.route("/status")
def status():
    """Displays the status of the project"""
    return {"status": "OK"}


@app_views.route("/stats")
def stats():
    """Displays informationnt of the project stats"""
    data = {}
    info = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User
        }
    for key, value in info.items():
        data[key] = storage.count(value)
    return data
