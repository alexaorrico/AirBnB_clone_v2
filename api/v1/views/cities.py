#!/usr/bin/python3
"""states"""

from models.state import State
from models.city import City
from flask import Flask, abort, jsonify, request
from models import storage
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """get cities"""
    li = []
    get_stat = storage.get(State, state_id)
    if not get_stat:
        abort(404)
    for item in get_stat.cities:
        li.append(item.to_dict())
    return jsonify(li)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_cities_by_id(city_id):
    """get by id"""
    get = storage.get(City, city_id)
    if not get:
        abort(404)
    return jsonify(get.to_dict())


@app_views.route('cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def del_cities(city_id):
    """delete city"""
    get = storage.get(City, city_id)
    if not get:
        abort(404)
    storage.delete(get)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def post_cities(state_id):
    """post city"""
    if not storage.get(State, state_id):
        abort(404)
    get_json = request.get_json()
    if not get_json:
        abort(400, "Not a JSON")
    if not get_json.get("name"):
        abort(400, "Missing name")
    new = City(**get_json)
    storage.new(new)
    storage.save()
    return jsonify(new.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """put in status"""
    get = storage.get(City, city_id)
    get_json = request.get_json()
    if not get:
        abort(404)
    if not get_json:
        abort(400, "Not a JSON")
    for k, v in get_json.items():
            if k not in ["id", "created_at", "updated_at", "state_id"]:
                setattr(get, k, v)
    storage.save()
    return jsonify(get.to_dict())
