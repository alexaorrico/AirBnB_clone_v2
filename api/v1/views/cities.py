#!/usr/bin/python3
"""view cities object"""

from sre_parse import State
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.state import State

@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def cities_by_states(state_id):
    """return list of all object cities"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = list()
    list_cities = storage.all('City')
    for value in list_cities.values():
        if state_id == value.state_id:
            cities.append(value.to_dict())
    return jsonify(cities)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def city_by_id(city_id):
    """Get cities by ID"""
    from models.city import City
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())
