#!/usr/bin/python3
"""Routes for cities"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities(state_id):
    """returns citys for a state given"""
    state_found = storage.get(State, state_id)
    if state_found is None:
        abort(404)
    list_of_cities = state_found.cities
    citys_dict = []
    for city in list_of_cities:
        citys_dict.append(city.to_dict())
    return jsonify(citys_dict)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """returns city of id given"""
    city_found = storage.get(City, city_id)
    if city_found is None:
        abort(404)
    return jsonify(city_found.to_dict()), 200


@app_views.route('/states/<state_id>/cities/', methods=['POST'])
def create_city(state_id):
    """create a city and links to state"""
    http_request = request.get_json(silent=True)
    if http_request is None:
        return 'Not a JSON', 400
    elif 'name' not in http_request.keys():
        return 'Missing name', 400
    elif storage.get(State, state_id) is None:
        abort(404)
    new_city = City(**http_request)
    new_city.state_id = state_id
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """updates given city"""
    found_city = storage.get(City, city_id)
    if found_city is None:
        return '', 404
    http_request = request.get_json
    if http_request is None:
        return 'Not a JSON', 400
    for key, values in http_request.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(found_city, key, values)
    storage.save()
    return jsonify(found_city.to_dict()), 200


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """delete city if id is found"""
    city_found = storage.get(City, city_id)
    if city_found is None:
        return '{}', 404
    storage.delete(city_found)
    storage.save()
    return jsonify({}), 200
