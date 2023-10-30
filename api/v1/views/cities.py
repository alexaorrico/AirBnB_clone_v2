#!/usr/bin/python3
''' new view for cities objects'''

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State
from models.city import City

@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities_by_state(state_id):
    """
    Retrieves the list of all City objects of a State.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """
    Retrieves a City object by ID.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    return jsonify(city.to_dict())
