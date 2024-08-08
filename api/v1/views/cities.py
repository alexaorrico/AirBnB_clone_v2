#!/usr/bin/python3
"""
Module defines view for City objects that handles all default
RESTFUL API actions.
"""
from models import storage
from models.city import City
from models.state import State
from flask import jsonify, abort, request
from werkzeug.exceptions import BadRequest
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_all_cities(state_id):
    """ Retrieves all the cities of a state """
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    city_list = [city.to_dict() for city in state_obj.cities]
    return jsonify(city_list)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """ Retrieves city object of a specified city_id """
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)

    return jsonify(city_obj.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """ Deletes city object """
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)

    storage.delete(city_obj)
    storage.save()

    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """ Creates city object"""
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)

    try:
        data = request.get_json()
        if 'name' not in data:
            abort(400, description='Missing name')
    except BadRequest:
        abort(400, description='Not a JSON')

    data['state_id'] = state_id
    city_obj = City(**data)
    storage.new(city_obj)
    storage.save()

    return jsonify(city_obj.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """ Updates city object """
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)

    try:
        data = request.get_json()
    except BadRequest:
        abort(400, description='Not a JSON')

    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(city_obj, key, value)

    storage.save()

    return jsonify(city_obj.to_dict()), 200
