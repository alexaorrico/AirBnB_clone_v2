#!/usr/bin/python3
"""variable app_views which is an instance of Blueprint"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from os import getenv


@app_views.route(
        '/states/<state_id>/cities',
        methods=['GET'],
        strict_slashes=False
        )
def cities_bystate(state_id):
    """return cities by states"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    list_cities = []
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        for city in state.cities:
            list_cities.append(city.to_dict())
    else:
        list_cities = state.cities()
    return jsonify(list_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def cities_byid(city_id):
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def cities_delete(city_id):
    """delete city by id"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/states/<state_id>/cities',
        methods=['POST'],
        strict_slashes=False
        )
def cities_post(state_id=None):
    """add new cities"""
    response = request.get_json()
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    if response is None:
        abort(400, description='Not a JSON')
    if 'name' not in response.keys():
        abort(400, description='Missing name')
    response['state_id'] = state_id
    new_city = City(**response)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def cities(city_id=None):
    """update city obj"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    response = request.get_json()
    if response is None:
        abort(400, description='Not a json')
    response.pop('id', None)
    response.pop('updated_at', None)
    response.pop('created_at', None)
    for key, value in response.items():
        setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
