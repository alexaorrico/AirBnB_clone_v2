#!/usr/bin/python3
"""City objects that handles all default RESTFul API actions
"""
from flask import request, jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def retrive_cities(state_id):
    """ retrieves the list of all City """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    city_list = [city.to_dict() for city in state.cities]
    return jsonify(city_list)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def retrive_city_id(city_id):
    """Retrives city id
    """
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Delete city
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    else:
        city.delete()
        storage.save()
        return make_response(jsonify({}), status=200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """ request post for city
    """
    state = storage.get('State', state_id)
    data = request.get_json()
    if not state:
        abort(404)
    elif not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    elif 'name' not in data:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    else:
        data['state_id'] = state_id
        new_city = City(**data)
        new_city.save()
        return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """ request put for city
    """
    city = storage.get(City, city_id)
    data = request.get_json()
    key_ignore = ['id', 'state_id', 'created_at', 'updated_at']
    if not city:
        abort(404)
    elif not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    else:
        for key, value in data.items():
            if key not in key_ignore:
                setattr(city, key, value)
        storage.save()
        return make_response(jsonify(city.to_dict()), 200)
