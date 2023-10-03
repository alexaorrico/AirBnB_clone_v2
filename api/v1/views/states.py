#!/usr/bin/python3
"""
The states module
"""
from models import storage
from flask import Blueprint, jsonify, request, abort
from models.state import State
from models.city import City

state_bp = Blueprint('states', __name__, url_prefix='/api/v1/states')


@state_bp.route('/', methods=['GET'], strict_slashes=False)
def get_states():
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states)


@state_bp.route('/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@state_bp.route('/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_state_cities(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    cities_list = []

    for city in state.cities:
        cities_list += [city.to_dict()]

    return jsonify(cities_list)


@state_bp.route('/<state_id>/cities', methods=['POST'], strict_slashes=False)
def post_state_cities(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    data = request.get_json()

    if not data:
        abort(400, description='Not a JSON')

    if 'name' not in data:
        abort(400, description='Missing name')

    data['state_id'] = state_id

    new_cities = City(**data)
    new_cities.save()

    return jsonify(new_cities.to_dict()), 201


@state_bp.route('/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({})


@state_bp.route('/', methods=['POST'], strict_slashes=False)
def create_state():
    data = request.get_json()
    if not data:
        abort(400, description='Not a JSON')
    if 'name' not in data:
        abort(400, description='Missing name')
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@state_bp.route('/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description='Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict())
