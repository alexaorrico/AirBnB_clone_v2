#!/usr/bin/python3
"""This module contains routes for app_views"""
from api.v1.views import app_views


@app_views.route('/status')
def status():
    return {'status': 'OK'}


@app_views.route('/stats')
def stats():
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models import storage
    from models.user import User
    return {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
        }
