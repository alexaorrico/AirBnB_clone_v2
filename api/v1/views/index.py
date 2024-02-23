#!/usr/bin/python3
"""/status route for API v1."""

from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity


@app_views.route('/status')
def status():
    """return status of the API as json response."""
    return {"status": "OK"}

@app_views.route('/stats')
def stats():
    """endpoint that retrieves the number of each objects by type"""
    return {"amenities": storage.count(Amenity),
            "cities": storage.count(City),
            "places": storage.count(Place),
            "reviews": storage.count(Review),
            "states": storage.count(State),
            "users": storage.count(User)}
