#!/usr/bin/python3
"""city endpoint"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State

@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_cities(state_id):
    """get cities"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = []
    cities_db = storage.all(City).values()
    for city in cities_db:
        if city.state_id == state_id:
            cities.append(city.to_dict())
    return jsonify(cities), 200

@app_views.route('/cities/<city_id>', strict_slashes=False)
def get_city(city_id):
    """get a specific city"""
    city = storage.get(City, city_id)
    if city is not None:
        return jsonify(city.to_dict())
    abort(404)
