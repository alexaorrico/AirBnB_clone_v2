#!/usr/bin/python3
""" A module defines a rule that returns the current state of the app """
from api.v1.views import app_views
from flask import jsonify
import models
from models.user import User
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.state import State
from models.review import Review


@app_views.route('/status', strict_slashes=False)
def status():
    """ This function returns the app's status as JSON. """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """ A function that displays the quantity of each kind of object """
    return jsonify({
        "amenities": models.storage.count(Amenity),
        "cities": models.storage.count(City),
        "places": models.storage.count(Place),
        "reviews": models.storage.count(Review),
        "states": models.storage.count(State),
        "users": models.storage.count(User)
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
