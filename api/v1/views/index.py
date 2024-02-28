#!/usr/bin/python3
"""this returns the staus of our api"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """this returns status"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"], strict_slashes=False)
def Somestats():
    """Retrieves the number of objects per each type"""
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.user import User
    from models.review import Review
    from models.state import State
    from models import storage
    import json

    obj = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return json.dumps(obj, indent=2)
