#!/usr/bin/python3
"""Module for handling cities in the API"""
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views


@app_views.route('/states/<string:state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(unique_state_id):
    """Retrieve city information for all cities in a specified state"""
    specified_state = storage.get("State", unique_state_id)
    if specified_state is None:
        abort(404)
    city_list = []
    for city_instance in specified_state.cities:
        city_list.append(city_instance.to_dict())
    return jsonify(city_list)


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(unique_city_id):
    """Retrieve city information for specified city"""
    specified_city = storage.get("City", unique_city_id)
    if specified_city is None:
        abort(404)
    return jsonify(specified_city.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(unique_city_id):
    """Deletes a city based on its unique_city_id"""
    specified_city = storage.get("City", unique_city_id)
    if specified_city is None:
        abort(404)
    specified_city.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states/<string:state_id>/cities/', methods=['POST'],
                 strict_slashes=False)
def post_city(unique_state_id):
    """Create a new city"""
    specified_state = storage.get("State", unique_state_id)
    if specified_state is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    city_kwargs = request.get_json()
    city_kwargs['state_id'] = unique_state_id
    new_city = City(**city_kwargs)
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(unique_city_id):
    """Update a city"""
    specified_city = storage.get("City", unique_city_id)
    if specified_city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(specified_city, attr, val)
    specified_city.save()
    return jsonify(specified_city.to_dict())
