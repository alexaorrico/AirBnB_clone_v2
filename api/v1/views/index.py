#!/usr/bin/python3
"""run flask server"""
from api.v1.views import app_views
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User
from models import storage


@app_views.route('/status')
def status_ok():
    return {'status': 'OK'}


@app_views.route('/stats')
def number_of_obj():
    return {"amenities": storage.count(Amenity),
            "cities": storage.count(City),
            "places": storage.count(Place),
            "reviews": storage.count(Review),
            "states": storage.count(State),
            "users": storage.count(User)}
