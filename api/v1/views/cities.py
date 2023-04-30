#!/usr/bin/python3

'''
This module contains views for the City class
Routes:
    GET /api/v1/states/<state_id>/cities - Retrieves all City objects
    GET /api/v1/cities/<city_id> - Retrieves a City object
    DELETE /api/v1/cities/<city_id> - Deletes a City object
    POST /api/v1/states/<state_id>/cities - Creates a City
    PUT /api/v1/cities/<city_id> - Updates a City object
'''

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    '''
    Retrieves the list of all City objects
    '''
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    '''
    Retrieves a City object from its id
    '''
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    '''
    Deletes a city object
    '''
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    '''
    Creates a City
    '''
    state = storage.get(State, state_id)
    body = request.get_json()
    if state is None:
        abort(404)
    if body is None:
        abort(400, 'Not a JSON')
    if 'name' not in body:
        abort(400, 'Missing name')
    body['state_id'] = state_id
    city = City(**body)
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    '''
    Updates a City Class
    '''
    city = storage.get(City, city_id)
    body = request.get_json()
    if city is None:
        abort(404)
    if body is None:
        abort(400, 'Not a JSON')
    for k, v in body.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(city, k, v)
    storage.save()
    return jsonify(city.to_dict()), 200
