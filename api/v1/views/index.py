#!/usr/bin/python3
"""
index
"""

from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from models.state import State
from models import storage


@app_views.route('/status')
def status_json():
    """ json status """
    return {"status": "OK"}


@app_views.route('/stats')
def stats():
    """ endpoint that retrieves the number of each objects by type """
    JSON = {"amenities": storage.count(Amenity),
            "cities": storage.count(City),
            "places": storage.count(Place),
            "reviews": storage.count(Review),
            "states": storage.count(State),
            "users": storage.count(User), }
    return JSON
