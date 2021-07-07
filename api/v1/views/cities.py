#!/usr/bin/python3
"""
View to handle all default RestFull API actions
"""


from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET'])
def get_tasks8(state_id):
    """Return the data of all cities"""
    state_by_id = storage.get(State, state_id)
    if state_by_id is None:
        abort(404)
    return jsonify([city.to_dict() for city in state_by_id.cities])


@app_views.route('/cities/<city_id>/', strict_slashes=False,
                 methods=['GET'])
def get_task8(city_id):
    """Return the data of a specific city"""
    city_by_id = storage.get(City, city_id)
    if city_by_id is None:
        abort(404)
    return jsonify(city_by_id.to_dict())


@app_views.route('/cities/<city_id>/', strict_slashes=False,
                 methods=['DELETE'])
def delete_task8(city_id):
    """Deleting a specific city by id"""
    city_by_id = storage.get(City, city_id)
    if city_by_id is None:
        abort(404)
    else:
        storage.delete(city_by_id)
        storage.save()
        return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=['POST'])
def post_task8(state_id):
    """Create new city"""
    state_by_id = storage.get(State, state_id)
    if state_by_id is None:
        abort(404)
    new_requ = request.get_json()
    if not new_requ:
        abort(400, 'Not a JSON')
    if 'name' not in new_requ:
        abort(400, 'Missing name')
    new_city = City(**request.get_json())
    new_city.state_id = state_id
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_task8(city_id):
    """Updating a city"""
    new_requ = request.get_json()
    if not new_requ:
        abort(400, 'Not a JSON')
    city_by_id = storage.get(City, city_id)
    if city_by_id is not None:
        for attr, value in request.get_json().items():
            setattr(city_by_id, attr, value)
        storage.save()
        return jsonify(city_by_id.to_dict()), 200
    abort(404)
