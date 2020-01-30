#!/usr/bin/python3
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_state_id_cities(state_id):
    """ Return the cities from a state id """
    catch_state = storage.get('State', state_id)
    if catch_state is None:
        abort(404)
    cities_list = []
    for city in catch_state.cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_id(city_id):
    """ Return the city form a id """
    catch_city = storage.get('City', city_id)
    if catch_city is None:
        abort(404)
    return jsonify(catch_city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def del_city_id(city_id):
    """ Delete the city form a id """
    catch_city = storage.get('City', city_id)
    if catch_city is None:
        abort(404)
    storage.delete(catch_city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def post_state_id_cities(state_id):
    """ Return cities associated with a state id """
    data = request.get_json()
    catch_state = storage.get('State', state_id)
    if catch_state is None:
        abort(404)
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    new_city = City(**data)
    new_city.state_id = state_id
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_cities_id(city_id):
    """ Return a city from a id passed"""
    catch_city = storage.get('City', city_id)
    if catch_city is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(catch_city, key, value)
    storage.save()
    return jsonify(catch_city.to_dict()), 200
