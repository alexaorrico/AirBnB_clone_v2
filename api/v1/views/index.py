#!/usr/bin/python3
""" Module for storing indeces for the route Blueprints. """
from api.v1.views.__init__ import app_views
from models.amenity import Amenity
from models.review import Review
from models.place import Place
from models.state import State
from models.city import City
from models.user import User
from models import storage


@app_views.route("/status")
def return_status():
    """ Returns the status of the api. """
    status = {"status": "OK"}
    return(status)


@app_views.route("/stats")
def return_stats():
    """ Returns the stats in numbers of the objects available. """
    classes = {"amenities": Amenity, "cities": City, "places": Place,
               "reviews": Review, "states": State, "users": User}
    stats = {}

    for key, obj in classes.items():
        stats[key] = storage.count(obj)

    return(stats)
