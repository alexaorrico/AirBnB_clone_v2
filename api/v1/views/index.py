#!/usr/bin/python3
""" The status code for the api """


from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def count():
    from models import storage
    from models.state import State
    from models.city import City
    from models.amenity import Amenity
    from models.place import Place
    from models.user import User
    from models.review import Review
    c_amenities = storage.count(Amenity)
    c_cities = storage.count(City)
    c_places = storage.count(Place)
    c_reviews = storage.count(Review)
    c_states = storage.count(State)
    c_users = storage.count(User)
    return jsonify({
        "amenities": c_amenities,
        "cities": c_cities,
        "places": c_places,
        "reviews": c_reviews,
        "states": c_states,
        "users": c_users
    })
