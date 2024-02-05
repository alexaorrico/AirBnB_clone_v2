#!/usr/bin/python3
""" index route"""

from . import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """ returna json string"""

    obj = {"status": "OK"}

    return jsonify(obj)


@app_views.route('/stats')
def type_count():
    """ an endpoint that retrieves the number of each objects by type"""

    from models.amenity import Amenity
    from models import storage
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User

    obj = {
            "amenities": storage.count(Amenity),
            "cities": storage.count(City),
            "places": storage.count(Place),
            "reviews": storage.count(Review),
            "states": storage.count(State),
            "users": storage.count(User)
        }

    return jsonify(obj), 200
