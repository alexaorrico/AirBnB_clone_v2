#!/usr/bin/python3
"""Creatte the states function"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
import models


@app_views.route('/states', methods=['GET'])
def get_all_states():
    """retrieves all state"""
    all_state = []
    for enu in models.storage.all("State").values():
        all_state.append(enu.to_dict())
    return jsonify(all_state)


@app_views.route('states/<state_id>', methods=['GET'])
def get_a_state_with_id(state_id):
    """get a state using id"""
    answer = models.storage.get("State", state_id)
    if answer:
        return jsonify(answer.to_dict())
    abort(404)


@app_views.route('states/<state_id>', methods=['DELETE'])
def delete_a_state_with_id(state_id):
    """delete a state using id"""
    answer = models.storage.get("State", state_id)
    if answer:
        answer.delete()
        models.storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/states', methods=['POST'])
def add_a_statesi():
    """create a state"""
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    values = request.get_json()
    new_state = State(**values)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('states/<state_id>', methods=['PUT'])
def update_a_state_with_id(state_id):
    """get a state using id"""
    answer = models.storage.get("State", state_id)
    if answer:
        if not request.json:
            return jsonify({"error": "Not a JSON"}), 400
        for k, v in request.get_json().items():
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(answer, k, v)
        answer.save()
        return jsonify(answer.to_dict()), 200
    abort(404)
