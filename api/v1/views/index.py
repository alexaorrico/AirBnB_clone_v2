#!/usr/bin/python3
"""
Defines status endpoint of this api
"""
from . import City
from . import User
from . import Place
from . import State
from . import Review
from . import Amenity
from . import app_views
from . import storage


@app_views.route("/status")
def status():
    """
    Returns a JSON status of the api
    """
    return {"status": "OK"}


@app_views.route("/stats")
def stats():
    """
    retrieves the number of each objects by Model
    """
    stats = {}
    clz = {"amenities": Amenity, "cities": City, "places": Place,
           "reviews": Review, "states": State, "users": User}
    for k, v in clz.items():
        stats[k] = storage.count(v)
    return stats
