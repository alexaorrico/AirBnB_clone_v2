#!/usr/bin/python3
""" Index File """

from api.v1.views import app_views
import json
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """ Returns Status of api"""

    status = {"status": "OK"}
    return json.dumps(status, indent=2)


@app_views.route('/api/v1/stats', strict_slashes=False)
def class_number():
    """Returns The Number of Each Individual Class"""
    dict_count = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "Places": storage.count(Places),
        "Review": storage.count(Review),
        "state": storage.count(State),
        "users": strorage.count(User)
    }
    return jsonify(dict_count)
