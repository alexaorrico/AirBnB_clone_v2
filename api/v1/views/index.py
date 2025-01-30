#!/usr/bin/python3
"""index file for views"""
from api.v1.views import app_views
from flask import jsonify, json, current_app


@app_views.route('/status')
def status():
    """route `/status` on the object app_views that returns a JSON"""
    o_dct = {"status": "OK"}
    return jsonify(o_dct)


@app_views.route('/stats')
def stats():
    """endpoint that retrieves the number of each objects by type"""
    from models import storage
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User
    stats_dict = {"amenities": storage.count(Amenity),
                  "cities": storage.count(City),
                  "places": storage.count(Place),
                  "reviews": storage.count(Review),
                  "states": storage.count(State),
                  "users": storage.count(User),
                  }
    return jsonify(stats_dict)
