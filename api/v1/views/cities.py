#!/usr/bin/python3
"""
    RESTful API action view handler for class City
"""

from api.v1.views import app_views
from flask import Flask, abort, jsonify, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_city_by_state(state_id):
    """returns the list of cities in state, json form"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    city_list = [c.to_dict() for c in state.cities]
    return jsonify(city_list), 200


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_id(city_id):
    """returns city and its matching id using GET"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict()), 200


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """DELETE city obj that matches the given city_id"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """creates new city obj via state association using POST method"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif "name" not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    else:
        obj_data = request.get_json()
        state = storage.get("State", state_id)
        if state is None:
            abort(404)
        obj_data['state_id'] = state.id
        obj = City(**obj_data)
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """updates existing city object using PUT method"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    obj = storage.get("City", city_id)
    if obj is None:
        abort(404)
    obj_data = request.get_json()
    obj.name = obj_data['name']
    obj.save()
    return jsonify(obj.to_dict()), 200
