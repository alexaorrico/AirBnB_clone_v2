#!/usr/bin/python3
"""Create in a  new city Objects to all default RESTful API"""
import models
from api.v1.views import app_views
from models import storage
from flask import jsonify, request, abort
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_all_city(state_id=None):
    """retrieves a list of all city objects of a given state"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    cities = storage.all("City")
    city_list = []
    for value in cities.values():
        if value.state_id == state_id:
            city_list.append(value.to_dict())

    return jsonify(city_list)


@app_views.route('cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id=None):
    """return individual city object"""
    obj = storage.get("City", city_id)
    if obj is None:
        abort(404)
    obj = obj.to_dict()
    return jsonify(obj)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id=None):
    """Delete each city"""
    obj = storage.get("City", city_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>', methods=['POST'], strict_slashes=False)
def create_city(state_id=None):
    """create city if not exists"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    args = request.get_json()
    if args is None:
        return jsonify({"error": "Not a JSON"}), 400
    elif "name" not in args:
        return jsonify({"error": "Missing name"}), 400
    args["stare_id"] = state_id
    obj = City(**args)
    state.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id=None):
    """Update each city"""
    obj = storage.get("City", city_id)
    if obj is None:
        abort(404)
    args = request.get_json()
    if args is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in args.items():
        if key not in ["id", "state_id", "update_at", "created_at"]:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200
