#!/usr/bin/python3
"""creates a new view for State Objects"""
from os import name
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.city import City
from models import storage
import json


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_city(state_id):
    """gets all state objects"""
    all_objects = storage.get(City, state_id)
    if all_objects is None:
        abort(404)
    single_object = []
    for city in all_objects.single_object:
        single_object.append(city.to_dict())
    return jsonify(single_object)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city_id(city_id):
    """gets the state object using his id"""
    all_objects = storage.get(City, city_id)
    if all_objects is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete(city_id=None):
    """Deletes"""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def post():
    """Creates"""
    res = request.get_json()
    if not res:
        abort(400, {"Not a JSON"})
    if 'name' not in res:
        abort(400, {"Missing name"})
    obj = State(name=res['name'])
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put(city_id=None):
    """PUT"""
    res = request.get_json()
    if not res:
        abort(400, {"Not a JSON"})
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    i_key = ["id", "created_at", "updated_at"]
    for key, value in res.items():
        if key not in i_key:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200
