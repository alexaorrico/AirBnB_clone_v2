#!/usr/bin/python3
"""
Create a route that returns a JSON
"""
from flask import Flask
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/api/v1/status', strict_slashes=False)
def return_status():
    """returns a JSON string"""
    return {"status": "OK"}


@app_views.route('/api/v1/stats', strict_slashes=False)
def count_objects():
    """retrieves the number of each object by type"""
    return {"amenities": storage.count(Amenity),
            "cities": storage.count(City),
            "places": storage.count(Place),
            "reviews": storage.count(Review),
            "states": storage.count(State),
            "users": storage.count(User)}
