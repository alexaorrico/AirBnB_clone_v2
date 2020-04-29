#!/usr/bin/python3
"""A new view for cities objects"""
from api.v1.views import app_views
from models import state, city, storage
from flask import Flask, jsonify, abort, request


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities(state_id):
    """Retrieves the list of all City"""
    get_state = storage.get('State', state_id)
    list_cities = []
    if get_state is None:
        abort(404)
    for city in get_state.cities:
        list_cities.append(city.to_dict())
    return jsonify(list_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_id(city_id):
    """Retrieves a City"""
    get_city = storage.get('City', city_id)
    if get_city:
        return jsonify(get_city.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def city_delete(city_id):
    """Deletes a City"""
    get_city = storage.get('City', city_id)
    if get_city:
        get_city.delete()
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def city_post(state_id):
    """Creates a City"""
    get_state = storage.get('State', state_id)
    if get_state is None:
        abort(404)
    if not request.get_json():
        return jsonify({'message': 'Not a JSON'}), 400
    if 'name' not in request.get_json():
        return jsonify({'message': 'Missing name'}), 400

    city = city.City(name=request.get_json().get('name'), state_id=state_id)
    state.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def city_put(city_id):
    """Updates a City"""
    get_city = storage.get('City', city_id)
    if get_city is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')

    for k, v in request.get_json().items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(get_city, k, v)
    get_city.save()
    return jsonify(get_city.to_dict())
