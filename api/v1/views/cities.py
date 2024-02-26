#!/usr/bin/python3
'''The cities.py module'''
from flask import abort, jsonify, request
from models.state import State
from models.city import City
from api.v1.views import app_views
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                    strict_slashes=False)
def get_cities_and_state(state_id):
    '''Retrieves the list of all City'''
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_cities(city_id):
    '''Retrieves a City object'''
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    else:
        return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    '''Deletes a City object'''
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    else:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                strict_slashes=False)
def create_city(state_id):
    '''Creates a City'''
    state = storage.get(City, state_id)
    if not state:
        return abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    data = request.get_json()
    if 'name' not in data:
        abort(400, 'Missing name')
    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return jsonify(cityto_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False))
def update_city(city_id):
    '''Updates a city objects'''
    city = storage.get(City, city_id)
    if city:
        if not request.get_json():
            abort(400, 'Not a JSON')
        data = request.get_json()
        ignore_key= ['id', 'state_id', 'created_at', 'updated_at']
        for ky, val in data.items():
            if ky not in ignore_key:
                setattr(city, ky, val)
        city.save()
        return jsonify(city.to_dict()), 200
    else:
        abort(404)


@ app_views.errorhandler(404)
def not_found(err):
    '''handle the error 404'''
    return jsonify({'error': 'Not found'}), 404
