#!/usr/bin/python3
"""Creatte the cities function"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.city import City
from models.state import State
import models


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_all_cities(state_id):
    """retrieves all cities linked to a state"""
    state = models.storage.get("State", state_id)
    if state:
        city = models.storage.all("City")
        all_city = []
        for ct in city.values():
            if ct.state_id == state_id:
                all_city.append(ct.to_dict())
        return jsonify(all_city)
    abort(404)


@app_views.route('cities/<city_id>', methods=['GET'])
def get_a_city_with_id(city_id):
    """get a city using id"""
    answer = models.storage.get("City", city_id)
    if answer:
        return jsonify(answer.to_dict())
    abort(404)


@app_views.route('cities/<city_id>', methods=['DELETE'])
def delete_a_city_with_id(city_id):
    """delete a state using id"""
    answer = models.storage.get("City", city_id)
    if answer:
        answer.delete()
        models.storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def add_a_city(state_id):
    """create a city"""
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    status = models.storage.get("State", state_id)
    if status is None:
        abort(404)
    values = request.get_json()
    new_state = State(**values)
    new_state.state_id = state_id
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('cities/<city_id>', methods=['PUT'])
def update_a_city_with_id(city_id):
    """get a city using id"""
    answer = models.storage.get("City", city_id)
    if answer:
        if not request.json:
            return jsonify({"error": "Not a JSON"}), 400
        for k, v in request.get_json().items():
            if k not in ['id', 'created_at', 'updated_at', 'state_id']:
                setattr(answer, k, v)
        answer.save()
        return jsonify(answer.to_dict()), 200
    abort(404)
