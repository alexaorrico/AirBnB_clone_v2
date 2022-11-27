#!/usr/bin/python3
"""handles default RESTful API actions for City objects"""
from api.v1.views import app_views
from flask import jsonify, request, abort, Flask, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_states_with_cities(state_id=None):
    """Retrieves a state along with it's cities"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def city_get_or_delete(city_id=None):
    """Retrieves a city or deletes a city"""
    city = storage.city(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(city.to_dict())
    elif request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)
    elif request.method == 'PUT':
        if request.is_json:
            city_data = request.get_json()
        else:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        ignore_list = ['id', 'created_at', 'updated_at', 'state_id']
        for key, val in city_data.items():
            if key not in ignore_list:
                setattr(city, key, val)
        storage.save()
        return make_response(jsonify(city.to_dict()), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def city_post(state_id=None):
    """creates a city"""
    city_data = request.get_json()
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not city_data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in city_data.keys():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_city = City(**city_data)
    storage.save()
    return make_response(jsonify(new_city.to_dict()), 201)
