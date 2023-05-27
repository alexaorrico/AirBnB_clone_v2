#!/usr/bin/python3
"""City objects that handle all default RESTFul API actions"""
from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    ls_cities = []
    if not state:
        abort(404)
    for city in state.cities:
        ls_cities.append(city.to_dict())
    return jsonify(ls_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """ Retrieves a specific city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a specific city Object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """Create a new city object"""
    data = request.get_json()
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not data:
        abort(400, description="Not a JSON")

    if 'name' not in data:
        abort(400, description="Missing name")

    new_city = City(**data)
    new_city.state_id = state_id
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """Updates a specific city by id"""
    city = storage.get(City, city_id)
    if city:
        data = request.get_json()
        if not data:
            abort(400, description="Not a JSON")

        ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(city, key, value)
        storage.save()
        return make_response(jsonify(city.to_dict()), 200)
    else:
        abort(404)
