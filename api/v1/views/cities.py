#!/usr/bin/python3
"""Module for handling cities in the API"""

# Import statements
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views


@app_views.route('/states/<string:state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """Get city information for all cities in a specified state"""
    state_instance = storage.get("State", state_id)
    if state_instance is None:
        abort(404)
    city_list = []
    for city_instance in state_instance.cities:
        city_list.append(city_instance.to_dict())
    return jsonify(city_list)


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """Get city information for the specified city"""
    city_instance = storage.get("City", city_id)
    if city_instance is None:
        abort(404)
    return jsonify(city_instance.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a city based on its city_id"""
    city_instance = storage.get("City", city_id)
    if city_instance is None:
        abort(404)
    city_instance.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states/<string:state_id>/cities/', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """Create a new city"""
    state_instance = storage.get("State", state_id)
    if state_instance is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    city_kwargs = request.get_json()
    city_kwargs['state_id'] = state_id
    new_city = City(**city_kwargs)
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """Update a city"""
    city_instance = storage.get("City", city_id)
    if city_instance is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attribute, value in request.get_json().items():
        if attribute not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city_instance, attribute, value)
    city_instance.save()
    return jsonify(city_instance.to_dict())
