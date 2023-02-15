#!/usr/bin/python3
"""
View for Cities that handles all RESTful API actions
"""

from flask import jsonify, request, abort
from models import storage
from models.city import City
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities_all(state_id):
    """ returns list of all City objects linked to a given State """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    cities_all = []
    cities = storage.all("City").values()
    for city in cities:
        if city.state_id == state_id:
            cities_all.append(city.to_json())
    return jsonify(cities_all)


@app_views.route('/cities/<city_id>', methods=['GET'])
def city_get(city_id):
    """ handles GET method """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    city = city.to_json()
    return jsonify(city)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def city_delete(city_id):
    """ handles DELETE method """
    empty_dict = {}
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify(empty_dict), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def city_post(state_id):
    """ handles POST method """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")
    city = City(**data)
    city.state_id = state_id
    city.save()
    city = city.to_json()
    return jsonify(city), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def city_put(city_id):
    """ handles PUT method """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for key, value in data.items():
        ignore_keys = ["id", "created_at", "updated_at"]
        if key not in ignore_keys:
            city.bm_update(key, value)
    city.save()
    city = city.to_json()
    return jsonify(city), 200
