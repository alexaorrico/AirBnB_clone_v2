#!/usr/bin/python3
""" retruns json response status of API """
from flask import Flask, abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    ''' gets the list of all City objects of a State '''
    state_object = storage.get(State, state_id)
    if state_object is None:
        abort(404)
    cities_list = [city.to_dict() for city in state_object.cities]
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_id(city_id):
    ''' gets specific state objects by its state ID '''
    city_object = storage.get(City, city_id)
    if city_object is None:
        abort(404)
    return jsonify(city_object.to_dict())


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    ''' deletes city object '''
    city_object = storage.get(City, city_id)
    if city_object is None:
        abort(404)
    storage.delete(city_object)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    '''' creates a city '''
    state_object = storage.get(State, state_id)
    if state_object is None:
        abort(404)
    response = request.get_json(silent=True)
    if not response:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in response:
        return make_response(jsonify({'error': 'Missing name'}), 400)

    new_city = City(**response)
    new_city.state_id = state_id
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    '''' updates a city object '''
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    response = request.get_json(silent=True)
    if response is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    for key, value in response.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return make_response(city.to_dict(), 200)
