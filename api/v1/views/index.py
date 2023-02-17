#!/usr/bin/python3
"""Index Package"""
from flask import jsonify
from models import storage
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """JSON response giving the api status
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def object_numb():
    """an endpoint that retrieves the number of each objects by type
    """
    info = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return jsonify(info)


if __name__ == "__main__":
    pass
