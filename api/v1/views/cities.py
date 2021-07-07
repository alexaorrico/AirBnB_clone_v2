#!/usr/bin/python3
"""States view module.."""
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request, make_response


@app_views.route('/cities', methods=['GET'], strict_slashes=False)
def all_cities():
    """Retrieves the list of all State objects"""
    cities_list = []
    states_objs = storage.all('City').values()
    for element in states_objs:
        cities_list.append(element.to_dict())
    return jsonify(cities_list)


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def cities_list(state_id):
    """Retrieves the list of all State objects"""
    cities_list = []
    cities_objs = storage.get('State', state_id)
    if cities_objs is None:
        abort(404)
    for city in cities_objs.cities:
        cities_list.append(city.to_dict())

    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def cities_list_id(city_id):
    """Retrieves a specific City object by Id"""
    cities_objs = storage.all('City').values()
    for element in cities_objs:
        if element.id == city_id:
            return jsonify(element.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def cities_remove(city_id):
    """Remove a state by Id"""
    city_to_delete = storage.get('City', city_id)
    if city_to_delete is None:
        abort(404)
    city_to_delete.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def new_city(state_id):
    """Creates a new state"""
    state_obj = storage.get('State', state_id)
    if state_obj is None:
        abort(404)
    city_data = request.get_json()
    if city_data is None:
        abort(400, "Not a JSON")
    if not city_data.get('name'):
        abort(400, "Missing name")
    city_data['state_id'] = state_id
    new_city = City(**city_data)
    storage.new(new_city)
    storage.save()
    storage.reload()
    return make_response(jsonify(new_city.to_dict())), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def city_update(city_id):
    """Updates one state based on its id"""
    forbiden_keys = ['id', 'created_at', 'updated_at', 'state_id']
    city_to_update = storage.get('City', city_id)
    if city_to_update is None:
        abort(404)
    data_for_update = request.get_json()
    if data_for_update is None:
        abort(400, "Not a JSON")
    for key, value in data_for_update.items():
        if key not in forbiden_keys:
            setattr(city_to_update, key, value)
    city_to_update.save()
    storage.reload()
    return jsonify(city_to_update.to_dict()), 200
