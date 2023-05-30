#!/usr/bin/python3
"""A new view for City objects that handles all default RESTFul API actions"""

from models import storage
from models.city import City
from models.state import State
from flask import jsonify, request, make_response, abort
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['GET', 'POST'])
def state_cities(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if request.method == 'GET':
        cities = [city.to_dict() for city in state.cities]
        return jsonify(cities)

    if request.method == 'POST':
        if not request.json:
            abort(400, 'Not a JSON')
        if 'name' not in request.json:
            abort(400, 'Missing name')
        new_city = City(**request.get_json())
        new_city.state_id = state_id
        new_city.save()
        return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def cities(city_id):
    """Retrieves a City object using city_id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if request.method == 'GET':
        return jsonify(city.to_dict())

    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        if not request.json:
            abort(400, 'Not a JSON')
        for k, v in request.json.items():
            if k not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city, k, v)
        city.save()
        return make_response(jsonify(city.to_dict()), 200)
