#!/usr/bin/python3
"""Import Modules"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def get_status():
    """Returns the app status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'],  strict_slashes=False)
def status():
    """Retrieves the number of objects per each type"""
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User
    from models import storage
    import json
    dictionary = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    json_dictionary = json.dumps(dictionary, indent=2)
    return json_dictionary
