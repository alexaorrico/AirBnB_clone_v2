#!/usr/bin/python3
""" view for City """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def retrieve_cities(state_id):
    """ function to retrieve related cities """
    if state_id is None:
        return abort(404)
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    cities = state.cities
    list_city = []
    for city in cities:
        list_city.append(city.to_dict())
    return jsonify(list_city)


@app_views.route('cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """ retrieves city by id """
    if city_id is None:
        return abort(404)
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    return jsonify(city.to_dict())


@app_views.route('cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """ function to delete city instance """
    if city_id is None:
        return abort(404)
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """ post a new city """
    if state_id is None:
        return abort(404)
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    if not request.json:
        return 'Not a JSON', 400
    if 'name' not in request.json:
        return 'Missing name', 400
    data = request.get_json()
    city = City(**data)
    city.state_id = state.id
    city.save()
    city_dict = city.to_dict()
    return jsonify(city_dict), 201


@app_views.route('cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """ update city instance """
    if city_id is None:
        return abort(404)
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    if not request.json:
        return 'Not a JSON', 400
    body = request.get_json()
    for key, value in body.items():
        if key == 'id' or key == 'created_at' or key == 'updated_at':
            continue
        setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
