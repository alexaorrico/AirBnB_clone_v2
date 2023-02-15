#!/usr/bin/python3

"""Bootstap for view"""

from api.v1.views import app_views
from models.amenity import Amenity 
from models.state import State
from models.city import City
from models.review import Review
from models.user import User
from models.place import Place
import models

@app_views.route('/status')
def status():
    """get status ok"""
    return {"status": "OK"}

@app_views.route("/stats")
def stats():
    """return all number of objects"""
    classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}
    res = {}
    for key, value in classes.items():
        res[key] = models.storage.count(value)
    return res

