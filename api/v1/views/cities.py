#!/usr/bin/python3
"""
Views for Ciy object
"""
from flask import jsonify, abort, request
from models import storage

from api.v1.views import app_views
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                strict_slashes=False)
def cities_by_state(state_id):
    """Retrieves the list of all city objects of a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def show_city(city_id):
    """Retrieves a city object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """ deletes a city object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def insert_city(state_id):
    """Creates a city"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    props = request.get_json()
    if type(props) != dict:
        abort(400, description="Not a JSON")
    if not props.get("name"):
        abort(400, description="Missing name")

    n_city = City(**props)
    n_city.state_id = state_id
    n_city.save()
    return jsonify(n_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """Updates a city objects"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if type(data) != dict:
        abort(400, description="Not a JSON")
    for k, v in data.items():
        if k not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, k, v)
    storage.save()
    return jsonify(city.to_dict()), 200
