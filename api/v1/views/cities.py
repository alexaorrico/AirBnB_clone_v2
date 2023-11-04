#!/usr/bin/python3
'''states.py'''
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities_by_state(state_id=None):
    '''get cities by state'''
    state = storage.get(State, state_id)
    if state:
        cities = []
        for city in state.cities:
            cities.append(city.to_dict())
        return jsonify(cities)
    else:
        abort(404)


@app_views.route('/cities', methods=['GET'], strict_slashes=False)
@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_cities(city_id=None):
    '''get cities'''
    if city_id:
        city = storage.get(City, city_id)
        if city:
            return jsonify(city.to_dict())
        else:
            abort(404)
    all_cities = []
    for city in storage.all('City').values():
        all_cities.append(city.to_dict())
    return jsonify(all_cities)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id=None):
    '''delete city'''
    city = storage.get(City, city_id)
    if city:
        city.delete()
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_cities(state_id=None):
    '''post cities'''
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in request.get_json():
        return jsonify({'error': 'Missing name'}), 400
    state = storage.get(State, state_id)
    if state:
        city = City(**request.get_json())
        city.state_id = state.id
        city.save()
        return jsonify(city.to_dict()), 201
    abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_cities(city_id=None):
    '''UPdate cities'''
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    city = storage.get(City, city_id)
    if city:
        (request.get_json()).pop('id', None)
        (request.get_json()).pop('updated_at', None)
        (request.get_json()).pop('created_at', None)
        (request.get_json()).pop('state_id', None)
        for key, value in request.get_json().items():
            setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict())
    else:
        abort(404)
