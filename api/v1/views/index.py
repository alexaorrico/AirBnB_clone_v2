#!/usr/bin/python3
""" Index to api to handle status and stats route"""
from api.v1.views import app_views
import flask
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', strict_slashes=False)
def status():
    """ return json with status OK"""
    return flask.jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """
    Endpoint that retrieves the number of each objects by type
    """
    stats = {"amenities": Amenity,
             "cities": City,
             "places": Place,
             "reviews": Review,
             "states": State,
             "users": User}
    for key, value in stats.items():
        stats[key] = storage.count(value)
    return flask.jsonify(stats)
