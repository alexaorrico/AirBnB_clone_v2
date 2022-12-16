#!/usr/bin/python3
""" City objects handles all default RESTFul API"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities_id(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if not state_id:
        abort(404, description="Not found")
    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities.to_dict())


@app_views.route('cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object. : GET /api/v1/cities/<city_id>"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())
