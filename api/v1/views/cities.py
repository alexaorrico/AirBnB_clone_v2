#!/usr/bin/python3
""" City objects handles all default RESTFul API"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states_all():
    """Retrieves the list of all State objects: GET /api/v1/states"""
    states = []
    for state in storage.all("State").values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities_id(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404, description="Not found")
    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities.to_dict())